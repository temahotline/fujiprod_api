from uuid import UUID
from users.dals import UserDAL, LicensorDAL
from users.schemas import UserCreate, ShowUser
from users.schemas import LicensorCreate, ShowLicensor


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            sign_up_source=body.sign_up_source,
            id_on_source=body.id_on_source,
        )
        return ShowUser(
            user_id=user.user_id,
            sign_up_source=user.sign_up_source,
            id_on_source=user.id_on_source,
        )


async def _get_user_by_id(user_id: UUID, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(user_id)
        if user is not None:
            return user


async def _create_new_licensor(body: LicensorCreate, session) -> ShowLicensor:
    async with session.begin():
        licensor_dal = LicensorDAL(session)
        licensor = await licensor_dal.create_licensor(
            user_id=body.user_id,
            full_name=body.full_name,
            birthday=body.birthday,
            passport_number=body.passport_number,
            passport_issue_date=body.passport_issue_date,
            registration=body.registration,
        )
        return ShowLicensor(
            licensor_id=licensor.licensor_id,
            user_id=licensor.user_id,
            full_name=licensor.full_name,
            birthday=licensor.birthday,
            passport_number=licensor.passport_number,
            passport_issue_date=licensor.passport_issue_date,
            registration=licensor.registration,
        )


async def _get_licensor_by_id(
        licensor_id: UUID, session) -> ShowLicensor:
    async with session.begin():
        licensor_dal = LicensorDAL(session)
        licensor = await licensor_dal.get_licensor_by_id(licensor_id)
        if licensor is not None:
            return licensor
