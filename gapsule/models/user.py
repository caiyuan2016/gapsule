import crypt
import re
import secrets
import asyncpg
import asyncio
from datetime import datetime
from gapsule import models
from gapsule.utils.log_call import log_call
from gapsule.utils.check_validity import check_mail_validity, check_password_validity, check_username_validity


@log_call()
def create_token(username, mail_address):
    if(check_username_validity(username) == True and check_mail_validity(mail_address) == True):
        pending_info = {}
        pending_info['username'] = username
        pending_info['mail_address'] = mail_address
        pending_info['token'] = secrets.token_urlsafe(16)
        models.signup_token.append_token(pending_info)
        return pending_info['token']


@log_call()
async def create_new_user(username, mail_address, password):
    if (check_username_validity(username) == False):
        return False
    if (check_mail_validity(mail_address) == False):
        return False
    if(check_password_validity(password) != False):
        temp = await models.connection.fetchrow(
            '''
        SELECT username FROM users_info
        WHERE username =$1''', username
        )
        if(temp != None):
            raise NameError()
        else:
            salt = crypt.mksalt()
            encrypted_password = crypt.crypt(password, salt)
            await models.connection.execute(
                '''
            INSERT INTO users_info(username, mail_address, password, salt) VALUES($1, $2, $3, $4)''', username, mail_address, encrypted_password, salt
            )
            return True
    else:
        return False


@log_call()
async def verify_user(username, password):
    if (check_username_validity(username) == False):
        return False
    if(check_password_validity(password) != False):
        temp_name = await models.connection.fetchrow(
            '''
            SELECT username FROM users_info
            WHERE username =$1
            ''',
            username
        )
        if(temp_name == None):
            raise NameError()
        else:
            temp_salt = await models.connection.fetchrow(
                '''
                SELECT salt FROM users_info
                WHERE username =$1
                ''',
                username
            )
            temp_encrypted_pw = crypt.crypt(password, salt=temp_salt['salt'])
            temp_password = await models.connection.fetchrow(
                '''
                SELECT password FROM users_info
                WHERE username =$1
                ''',
                username
            )
            if(temp_encrypted_pw == temp_password['password']):
                return True
            else:
                return False


@log_call()
async def set_profile(username, icon_url, introduction):
    if (check_username_validity(username) == False):
        return False
    else:
        temp_name = await models.connection.fetchrow(
            '''
        SELECT username FROM users_info
        WHERE username =$1
            ''',
            username
        )
        if(temp_name == None):
            raise NameError()
        else:
            temp_name = await models.connection.fetchrow(
                '''
            SELECT username FROM profiles
            WHERE username =$1
            ''',
                username
            )
            if(temp_name == None):
                await models.connection.execute(
                    '''
                    INSERT INTO profiles(username, icon_url, introduction) VALUES($1, $2, $3)
                    ''', username, icon_url, introduction
                )
            else:
                await models.connection.execute(
                    '''
                    UPDATE profiles
                    SET icon_url = $1, introduction = $2
                    WHERE username = $3
                    ''', icon_url, introduction, username
                )  # update
            return True


@log_call()
async def get_icon_url(username):
    url = await models.connection.fetchrow(
        '''
                SELECT icon_url FROM profiles
                WHERE username =$1
                ''',
        username
    )
    if (url == None):
        raise NameError()
    else:
        return url['icon_url']


@log_call()
async def get_introduction(username):
    url = await models.connection.fetchrow(
        '''
                SELECT introduction FROM profiles
                WHERE username =$1
                ''',
        username
    )
    if (url == None):
        raise NameError()
    else:
        return url['introduction']


@log_call()
def add_user_pending_verifying(username, email, password):
    return 'Token'


async def alter_username(old_username, new_username):
    if(check_username_validity(new_username) == False or check_username_validity(old_username) == False):
        raise NameError()
    else:
        temp_name = await models.connection.fetchrow(
            '''
        SELECT username FROM users_info
        WHERE username =$1
            ''',
            old_username
        )
        if(temp_name == None):
            raise NameError()
        else:
            await models.connection.execute(
                '''
                    UPDATE users_info
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username
            )
            await models.connection.execute(
                '''
                    UPDATE profiles
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username
            )
            return True


@log_call()
async def alter_icon(username, new_url):
    await models.connection.execute(
        '''
            UPDATE  profiles
            SET icon_url = $1
            WHERE username = $2
        ''', new_url, username
    )
    return True


@log_call()
async def alter_introduction(username, new_intro):
    await models.connection.execute(
        '''
            UPDATE  profiles
            SET introduction = $1
            WHERE username = $2
        ''', new_intro, username
    )
    return True


@log_call()
def creat_new_repo(reponame, description, visibility):
    return True


async def user_login(username, password):
    flag = await verify_user(username, password)
    if(flag == True):
        temp = await models.connection.fetchrow(
            '''
        SELECT username FROM log_info
        WHERE username =$1''', username
        )
        if(temp != None):
            await models.connection.execute(
                '''
            DELETE FROM log_info WHERE username=$1
            ''', username)
        session = secrets.token_urlsafe()
        await models.connection.execute(
            '''
                INSERT INTO log_info(username,session,login_time) VALUES($1,$2,$3)
            ''', username, session, datetime.now()
        )
        return session
    else:
        return False


@log_call()
async def check_session_status(username, session):
    return True


@log_call()
def sign_out():
    return True
