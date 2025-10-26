from datetime import datetime

from shared.logger import logger


def get_day(args, day_num: int | None) -> int | None:
    if day_num:
        pass
    else:
        if len(args) >= 1:
            try:
                day_num = int(args[1])
            except ValueError:
                logger.error('Please provide a valid day number.')
                return None
        else:
            now = datetime.now()
            if now.month == 12:
                day_num = now.day
            else:
                logger.error('🗓️ Not December! Please specify a day manually.')
                return None
    if day_num in range(1, 25):
        return day_num
    else:
        logger.error('🗓️ Day not in range! Please specify a day manually.')
        return None
