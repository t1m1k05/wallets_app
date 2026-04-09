from decimal import Decimal

from app.models import User, Wallet


def test_add_expense_success(db_session, client):
    # arrange - подготовь
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # act - выполни
    response = client.post(
        '/api/v1/operations/expense',
        json={
            'wallet_name': 'card',
            'amount': 50.0,
            'description': 'Food'
        },
        headers={"Authorization": f'Bearer {user.login}'}
    )


    #assert - проверь

    assert response.status_code == 200
    assert response.json()['message'] == 'Expense added'
    assert response.json()['wallet'] == wallet.name
    assert Decimal(str(response.json()['amount'])) == Decimal(50.0)
    assert response.json()['description'] == 'Food'
    assert Decimal(str(response.json()['new_balance'])) == Decimal(150.0)


def test_add_expense_negative_amount(db_session, client):
    # arrange - подготовь
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)


    # act - выполни
    response = client.post(
        '/api/v1/operations/expense',
        json={
            'wallet_name': 'card',
            'amount': -50.0,
            'description': 'Food'
        },
        headers={"Authorization": f'Bearer {user.login}'}
    )

    assert response.status_code == 422

def test_add_expense_empty_name(db_session, client):
    # arrange - подготовь
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # act - выполни
    response = client.post(
        '/api/v1/operations/expense',
        json={
            'wallet_name': '    ',
            'amount': 50.0,
            'description': 'Food'
        },
        headers={"Authorization": f'Bearer {user.login}'}
    )

    assert response.status_code == 422

def test_add_expense_unexist_wallet(db_session, client):
    # arrange - подготовь
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    db_session.commit()

    # act - выполни
    response = client.post(
        '/api/v1/operations/expense',
        json={
            'wallet_name': "chicha",
            'amount': 50.0,
            'description': 'Food'
        },
        headers={"Authorization": f'Bearer {user.login}'}
    )

    assert response.status_code == 404


def test_add_expense_unauthorized(client):
    # arrange - подготовь

    # act - выполни
    response = client.post(
        '/api/v1/operations/expense',
        json={
            'wallet_name': "chicha",
            'amount': 50.0,
            'description': 'Food'
        },
        headers={"Authorization": f'Bearer notexists'}
    )

    assert response.status_code == 401


def test_add_expense_not_enough_money(db_session, client):
    # arrange - подготовь
    user = User(login='test')
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # act - выполни
    response = client.post(
        '/api/v1/operations/expense',
        json={
            'wallet_name': 'card',
            'amount': 1150.0,
            'description': 'Food'
        },
        headers={"Authorization": f'Bearer {user.login}'}
    )


    #assert - проверь

    assert response.status_code == 400
