from bson import ObjectId

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj