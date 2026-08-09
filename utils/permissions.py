ADMIN = "admin"

MANAGER = "manager"

STAFF = "staff"

GM = "gm"

ACTOR = "actor"


# ==========================================================
# ROLE CHECK
# ==========================================================

def is_admin(

    user,

):

    return (

        user

        and

        user.role == ADMIN

    )


def is_manager(

    user,

):

    return (

        user

        and

        user.role in (

            ADMIN,

            MANAGER,

        )

    )


def is_staff(

    user,

):

    return (

        user

        and

        user.role in (

            ADMIN,

            MANAGER,

            STAFF,

            GM,

            ACTOR,

        )

    )


# ==========================================================
# ACCESS
# ==========================================================

def can_manage_games(

    user,

):

    return is_manager(

        user

    )


def can_manage_sessions(

    user,

):

    return is_manager(

        user

    )


def can_manage_finance(

    user,

):

    return is_admin(

        user

    )


def can_manage_staff(

    user,

):

    return is_admin(

        user

    )


def can_view_reports(

    user,

):

    return is_manager(

        user

    )