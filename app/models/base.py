"""
数据库基础模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from app.utils.database import Base


class BaseModel(Base):
    """数据库基础模型类"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    is_deleted = Column(Boolean, default=False, comment="是否删除")
    
    def to_dict(self, include_relationships: list = None) -> dict:
        """转换为字典
        
        Args:
            include_relationships: 要包含的关联关系列表
            
        Returns:
            dict: 字典形式的数据
        """
        # 序列化基本字段
        result = {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
        
        # 序列化关联数据
        if include_relationships:
            for rel_name in include_relationships:
                if hasattr(self, rel_name):
                    rel_value = getattr(self, rel_name)
                    if rel_value is not None:
                        if isinstance(rel_value, list):
                            # 一对多或多对多关系
                            result[rel_name] = [
                                item.to_dict() if hasattr(item, 'to_dict') else str(item)
                                for item in rel_value
                            ]
                        else:
                            # 一对一关系
                            result[rel_name] = rel_value.to_dict() if hasattr(rel_value, 'to_dict') else str(rel_value)
        
        return result