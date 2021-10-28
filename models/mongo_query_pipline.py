from datetime import datetime
from models.enums import ReportTypeEnum


class MongoPipline:

    @staticmethod
    def get_user_reports_dates_pipline(user_id, user_program_id):
        pipline = [
            {
                "$match": {
                    "user_program_id": user_program_id
                }
            },
            {"$sort": {"interval_start": 1}},
            {
                "$group" : {
                    "_id": {
                        "month": {"$month": "$created_at"},
                        "day": {"$dayOfMonth": "$created_at"},
                        "week": {"$ceil": {"$divide": [{"$dayOfMonth": "$created_at"}, 7]}},
                        "year": {"$year": "$created_at"}
                    }
                }
            }
        ]


