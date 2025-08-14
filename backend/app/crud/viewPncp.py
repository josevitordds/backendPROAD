from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import schemas 

def get_dados_da_view(
    db: Session,
    ano: Optional[int] = None,
    numero_processo: Optional[str] = None, 
    descricao_tr: Optional[str] = None    
) -> List[schemas.MinhaViewORM]:
    query = db.query(schemas.MinhaViewORM) 
    
    if ano is not None:
        query = query.filter(schemas.MinhaViewORM.ano_compra == ano) 
    
    if numero_processo is not None:
        query = query.filter(schemas.MinhaViewORM.processo.ilike(f"%{numero_processo}%")) 
    
    if descricao_tr is not None:
        query = query.filter(schemas.MinhaViewORM.objeto_TR.ilike(f"%{descricao_tr}%"))
        
    return query.all()

def get_dado_da_view_by_id(db: Session, id_unico: str) -> Optional[schemas.MinhaViewORM]:
    return db.query(schemas.MinhaViewORM).filter(schemas.MinhaViewORM.id_compra == id_unico).first()


