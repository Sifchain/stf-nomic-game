from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from nomic.database import SessionLocal, engine
from nomic.database.models.game import Game
from nomic.database.models.game_player import GamePlayer
from nomic.database.models.player_action import PlayerAction
from nomic.database.models.rule import Rule
from nomic.database.models.rule_proposal import RuleProposal
from nomic.database.models.rule_proposal_vote import RuleProposalVote
from nomic.database.models.user import User
from nomic.utils.roll_dice import roll_dice


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
        # Attempt to execute a simple SELECT 1 to check if the connection is alive
        db.execute(text("SELECT 1"))
        yield db
    except OperationalError:
        # If an OperationalError is caught, dispose the current db pool
        engine.dispose()
        db = SessionLocal()  # Create a new session after disposing the old one
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


def create_game(db: Session, game_name: str, initial_rules: str, creator: User) -> Game:
    # Create the game
    game = Game(name=game_name, status="CREATED", created_by=creator.id)
    db.add(game)
    db.commit()
    db.refresh(game)

    # Add initial rules to the game if provided
    if initial_rules:
        # split initial_rules into a list of rule names
        initial_rules_list = initial_rules.split(",")
        rules = [
            Rule(game_id=game.id, name=rule_name, description="")
            for rule_name in initial_rules_list
        ]
        # Add the rules to the database
        for rule in rules:
            db.add(rule)
    db.commit()
    db.refresh(game)

    return game


def join_game(db: Session, game: Game, player: User) -> Game:
    game_player = GamePlayer(game_id=game.id, user_id=player.id, score=0)
    db.add(game_player)
    db.commit()
    db.refresh(game)
    return game


def start_game(db: Session, game: Game) -> Game:
    game.status = "STARTED"  # type: ignore
    game.current_player_id = game.players[0].user_id
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
    game_player = (
        db.query(GamePlayer)
        .filter(
            GamePlayer.game_id == rule_proposal.game.id, GamePlayer.user_id == user_id
        )
        .first()
    )
    if not game_player:
        raise ValueError("User not part of the game")

    if user in rule_proposal.votes:
        raise ValueError("User has already voted")

    # Record the new vote
    rule_proposal_vote = RuleProposalVote(
        rule_proposal_id=rule_proposal_id, user_id=user_id, vote_type=vote_type
    )
    db.add(rule_proposal_vote)
    db.commit()
    return rule_proposal


def check_actions_match(db: Session, game: Game) -> bool:
    # Fetch all current rules in the game
    rule_ids = {str(rule.id) for rule in game.rules}

    # Fetch all actions taken in this turn
    actions = (
        db.query(PlayerAction)
        .filter(PlayerAction.game_id == game.id, PlayerAction.turn == game.current_turn)
        .all()
    )
    action_rule_ids = {str(action.rule_id) for action in actions}

    # Check if all actions match the current rules and vice versa
    if rule_ids == action_rule_ids:
        return True

    return False


def end_turn(
    db: Session, game: Game, game_player: GamePlayer
) -> tuple[Game, GamePlayer, int]:
    actions_match = check_actions_match(db, game)

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
            if actions_match:
                proposal.status = "VOTING"
            else:
                proposal.status = "CANCELLED"

    score = roll_dice()

    # Check win condition
    if actions_match:
        game_player.score += score  # type: ignore

        if game_player.score >= 100:
            game.status = "ENDED"  # type: ignore
            game.winner_id = game_player.user_id

    # Rotate turn to the next player
    players: List[User] = game.players
    current_index = players.index(game_player)  # type: ignore
    next_index = (current_index + 1) % len(players)
    game.current_player_id = players[next_index].user_id
    game.current_turn += 1  # type: ignore

    db.commit()
    db.refresh(game)
    db.refresh(game_player)

    return game, game_player, score


def take_action(db: Session, game_id: str, rule_id: str, user_id: str) -> None:
    game = db.get(Game, game_id)

    # Record the action
    player_action = PlayerAction(
        game_id=str(game_id),
        user_id=str(user_id),
        rule_id=str(rule_id),
        turn=game.current_turn if game else 0,
    )
    db.add(player_action)
    db.commit()


def get_rule_by_id(db: Session, rule_id: str) -> Rule | None:
    return db.get(Rule, rule_id)
