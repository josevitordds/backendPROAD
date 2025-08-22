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

def update_dado_da_view(db: Session, id_compra: str, dado_update: schemas.MinhaViewUpdate) -> Optional[schemas.MinhaViewORM]:
    update_data = dado_update.model_dump(exclude_unset=True)
    
    numero_item = update_data.get("numero_item_compra")
    if numero_item is None:
        return None

    contratacao = db.query(schemas.ContratacaoORM).filter(schemas.ContratacaoORM.id_compra == id_compra).first()
    if not contratacao:
        return None 

    contratacao_fields = [
        'processo', 'modalidade_nome', 'numero_compra', 'objeto_compra', 
        'ano_compra', 'valor_estimado', 'valor_homologado'
    ]
    has_update = False
    for key, value in update_data.items():
        if key in contratacao_fields and hasattr(contratacao, key):
            setattr(contratacao, key, value)
            has_update = True

    item_contratacao = db.query(schemas.ItensContratacoesORM).filter_by(id_compra=id_compra, numero_item_compra=numero_item).first()
    
    item_fields = [
        'descricao_resumida', 'unidade_medida', 'quantidade_resultado', 'quantidade_ufca',
        'valor_total_resultado', 'valor_unitario_estimado', 'valor_unitario_resultado',
        'codigo_fornecedor', 'nome_fornecedor', 'situacao_compra_item_nome', 
        'nome_material_ou_servico', 'descricao_detalhada'
    ]
    if item_contratacao:
        for key, value in update_data.items():
            if key in item_fields and hasattr(item_contratacao, key):
                setattr(item_contratacao, key, value)
                has_update = True
    
    if has_update:
        db.commit()
        return get_dado_da_view_by_id(db, id_unico=id_compra)
    
    return get_dado_da_view_by_id(db, id_unico=id_compra)

def delete_dado_da_view(db: Session, id_compra: str, numero_item_compra: int) -> Optional[schemas.ItensContratacoesORM]:
    item_para_deletar = db.query(schemas.ItensContratacoesORM).filter_by(id_compra=id_compra, numero_item_compra=numero_item_compra).first()

    if not item_para_deletar:
        return None

    db.delete(item_para_deletar)
    db.commit()
    
    return item_para_deletar
