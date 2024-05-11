# def create_all_tables():
      
#   from backend.models import Base
#   try:
#     print("trying to initialize db...")
#     db_engine = create_db_engine()
#     Base.metadata.drop_all(db_engine)
#     Base.metadata.create_all(db_engine)
    
#     print("created db models")
#   except Exception as e:
#     print("Error while trying to init db")
#     print(e)
  



# if __name__ == "__main__":
    
#     try:
#        create_all_tables()
#     except:
#         pass
    