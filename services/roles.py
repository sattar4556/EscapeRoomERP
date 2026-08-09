from database.crud import get_user_roles


async def is_admin(user_id):

    roles = await get_user_roles(user_id)

    for role in roles:

        if role.role_id == 1:
            return True

    return False


async def is_manager(user_id):

    roles = await get_user_roles(user_id)

    for role in roles:

        if role.role_id == 2:
            return True

    return False


async def is_gamemaster(user_id):

    roles = await get_user_roles(user_id)

    for role in roles:

        if role.role_id == 3:
            return True

    return False


async def is_actor(user_id):

    roles = await get_user_roles(user_id)

    for role in roles:

        if role.role_id == 4:
            return True

    return False