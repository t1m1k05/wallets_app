from decimal import Decimal

from tests.conftest import user_and_wallet


def test_add_expense_success(client, user_and_wallet):
    # arrange - подготовь
    user, wallet = user_and_wallet

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


def test_add_expense_negative_amount(user_and_wallet, client):
    # arrange - подготовь
    user, wallet = user_and_wallet

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

def test_add_expense_empty_name(user_and_wallet, client):
    # arrange - подготовь
    user, wallet = user_and_wallet

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

def test_add_expense_unexist_wallet(user_and_wallet, client):
    # arrange - подготовь
    user, wallet = user_and_wallet

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


def test_add_expense_not_enough_money(user_and_wallet, client):
    # arrange - подготовь
    user, wallet = user_and_wallet


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


def test_add_income_success(user_and_wallet, client):
    # arrange
    user, wallet = user_and_wallet

    # act
    response = client.post(
        "api/v1/operations/income",
        json={
            'wallet_name': 'card',
            'amount': 50.0,
            'description': 'Food'
        },
        headers={"Authorization": f'Bearer {user.login}'}
    )

    # assert
    assert response.status_code == 200
    assert response.json()['message'] == 'Income added'
    assert response.json()['wallet'] == 'card'
    assert Decimal(str(response.json()['amount'])) == Decimal(50.0)
    assert response.json()['description'] == "Food"
    assert Decimal(str(response.json()['new_balance'])) == Decimal(250.0)