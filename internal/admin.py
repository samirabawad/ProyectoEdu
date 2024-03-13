from fastapi import APIRouter

#aca irán las funcionalidades de editar y eliminar registros, usuarios y refrigeradores
#deberia darle la funcionalidad tambien de crear y visualizar

router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
    
