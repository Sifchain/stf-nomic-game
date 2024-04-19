from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional

from sqlalchemy import insert
from sqlalchemy.orm import Session

from nomic.database import SessionLocal, engine
from nomic.database.models.game import Game
from nomic.database.models.rule import Rule
from nomic.database.models.rule_proposal import RuleProposal
from nomic.database.models.rule_proposal_vote import RuleProposalVote
from nomic.database.models.user import User


class DatabaseHandler:
    def __init__(self):
        self.engine = engine

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def transform_created_at(self, created_at: Optional[datetime] = None) -> str:
        if not created_at:
            created_at = datetime.utcnow()

        return created_at.strftime("%Y-%m-%d %H:%M:%S")


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.get(User, user_id)


def create_user(db: Session, username: str, hashed_password: str) -> User:
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_game(db: Session, game_name: str, creator: User) -> Game:
    game = Game(name=game_name, status="CREATED", created_by=creator.id)
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def join_game(db: Session, game: Game, player: User) -> Game:
    game.players.append(player)
    db.commit()
    db.refresh(game)
    return game


def start_game(db: Session, game: Game) -> Game:
    game.status = "STARTED"  # type: ignore
    game.turn = game.players[0].id
    db.commit()
    db.refresh(game)
    return game


def get_game_by_id(db: Session, game_id: str) -> Game | None:
    return db.get(Game, game_id)


def check_player_in_game(game: Game, player: User) -> bool:
    return player in game.players


def create_rule_proposal(
    db: Session, game_id: str, user_id: str, name: str, description: str
) -> RuleProposal:
    rule_proposal = RuleProposal(
        game_id=game_id, proposed_by=user_id, name=name, description=description
    )
    db.add(rule_proposal)
    db.commit()
    db.refresh(rule_proposal)
    return rule_proposal


def vote_rule_proposal(
    db: Session, rule_proposal_id: str, user_id: str, vote_type: str
) -> RuleProposal:
    rule_proposal = db.get(RuleProposal, rule_proposal_id)
    user = db.get(User, user_id)
    if not rule_proposal:
        raise ValueError("Rule proposal not found")
    if not user:
        raise ValueError("User not found")
    if user not in rule_proposal.game.players:
        raise ValueError("User not part of the game")

    if user in rule_proposal.votes:
        raise ValueError("User has already voted")

    # Record the new vote
    db.execute(
        insert(RuleProposalVote).values(
            rule_proposal_id=rule_proposal_id, user_id=user_id, vote_type=vote_type
        )
    )

    db.commit()
    return rule_proposal


def end_turn(db: Session, game: Game) -> Game:
    # Rotate turn to the next player
    players: List[User] = game.players
    user = get_user_by_id(db, game.turn)
    current_index = players.index(user)
    next_index = (current_index + 1) % len(players)
    game.turn = players[next_index].id

    # Process rule proposals
    for proposal in game.rule_proposals:
        if proposal.status == "VOTING":
            yes_votes = sum(1 for vote in proposal.votes if vote.vote_type == "yes")
            no_votes = sum(1 for vote in proposal.votes if vote.vote_type == "no")
            if yes_votes > no_votes:
                # Create new rule
                new_rule = Rule(
                    game_id=game.id,
                    name=proposal.name,
                    description=proposal.description,
                )
                db.add(new_rule)
                proposal.status = "PASSED"
            else:
                proposal.status = "REJECTED"
        elif proposal.status == "CREATED":
            proposal.status = "VOTING"

    db.commit()
    db.refresh(game)

    return game
