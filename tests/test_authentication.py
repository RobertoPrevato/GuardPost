import pytest
from pytest import raises
from tests.examples import Request
from guardpost.authentication import Identity, User
from guardpost.asynchronous.authentication import AuthenticationHandler, AuthenticationStrategy


def test_claims():
    a = Identity({
        'oid': 'bc5f60df-4c27-49c1-8466-acf32618a6d2'
    })

    assert a.claims['oid'] == 'bc5f60df-4c27-49c1-8466-acf32618a6d2'


def test_authenticated():
    a = Identity({
        'oid': 'bc5f60df-4c27-49c1-8466-acf32618a6d2'
    }, 'JWT Bearer')

    assert a.authentication_mode == 'JWT Bearer'
    assert a.is_authenticated()


def test_not_authenticated():
    a = Identity({
        'oid': 'bc5f60df-4c27-49c1-8466-acf32618a6d2'
    })

    assert a.authentication_mode is None
    assert a.is_authenticated() is False


def test_user_claims_shortcut():
    a = User({
        'id': '001',
        'name': 'Charlie Brown',
        'email': 'charlie.brown@peanuts.eu'
    })

    assert a.id == '001'
    assert a.name == 'Charlie Brown'
    assert a.email == 'charlie.brown@peanuts.eu'


def test_has_claim():
    a = Identity({
        'oid': 'bc5f60df-4c27-49c1-8466-acf32618a6d2'
    })

    assert a.has_claim('oid')
    assert a.has_claim('foo') is False


def test_identity_dictionary_notation():
    a = Identity({
        'oid': 'bc5f60df-4c27-49c1-8466-acf32618a6d2'
    })

    assert a['oid'] == 'bc5f60df-4c27-49c1-8466-acf32618a6d2'
    assert a['foo'] is None


def test_user_identity_dictionary_notation():
    a = Identity({
        'oid': 'bc5f60df-4c27-49c1-8466-acf32618a6d2'
    })

    assert a['oid'] == 'bc5f60df-4c27-49c1-8466-acf32618a6d2'
    assert a['foo'] is None


def test_has_claim_value():
    a = Identity({
        'hello': 'world',
        'foo': 'foo'
    })

    assert a.has_claim_value('foo', 'foo')
    assert a.has_claim_value('hello', 'world')
    assert a.has_claim_value('hello', 'World') is False


def test_claims_default():
    a = Identity({})

    assert a.claims.get('oid') is None


@pytest.mark.asyncio
async def test_authentication_strategy():

    class ExampleHandler(AuthenticationHandler):

        async def authenticate(self, context: Request):
            # NB: imagine a web request with headers, and we authenticate the user
            # by parsing and validating a JWT token
            user = User({'id': context.headers['user']})
            context.user = user
            return user

    strategy = AuthenticationStrategy(ExampleHandler())

    request = Request({
        'user': 'xxx'
    })

    await strategy.authenticate(request)

    assert isinstance(request.user, User)
    assert request.user['id'] == 'xxx'


@pytest.mark.asyncio
async def test_strategy_throws_for_missing_context():

    strategy = AuthenticationStrategy()

    with raises(ValueError):
        await strategy.authenticate(None)