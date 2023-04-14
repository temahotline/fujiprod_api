from uuid import UUID

from src.licensor.dals import LicensorDAL
from src.licensor.schemas import LicensorCreate, ShowLicensor
from src.users.models import User


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
        user = await session.get(User, licensor.user_id)
        return ShowLicensor(
            licensor_id=licensor.licensor_id,
            user_id=licensor.user_id,
            user=user,
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


async def _update_licensor(
        updated_licensor_params: dict,
        licensor_id: UUID,
        session) -> UUID:
    async with session.begin():
        licensor_dal = LicensorDAL(session)
        updated_licensor_id = await licensor_dal.update_licensor(
            licensor_id, **updated_licensor_params
        )
        if updated_licensor_id is not None:
            return updated_licensor_id
