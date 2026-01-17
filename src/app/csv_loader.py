# Import pandas - the industry-standard library for data manipulation
import pandas as pd

# Import Path for file path operations
from pathlib import Path

# Import type hints for better code documentation and IDE support
from typing import Dict, List, Any

class CSVLoader:

    @staticmethod
    def validate_csv(filepath: Path) -> Dict[str, Any]:
        
        try:
            df = pd.read_csv(filepath)

            if df.empty:
                return {
                    "valid": False, 
                    "error": "CSV file is empty."
                    }
            
            if len(df.columns) == 0: 
                return {
                    "valid": False, 
                    "error": "CSV file has no columns."
                    }
            
            return {
                    "valid": True, 
                    "rows": len(df),
                    "columns": list(df.columns),
                    "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
                    }
            
        except Exception as e:
            return {
                "valid": False, 
                "error": str(e)
                }
        
    @staticmethod
    def load_csv(filepath: Path) -> pd.DataFrame:

        return pd.read_csv(filepath)
    
    @staticmethod
    def infer_schema(df: pd.DataFrame) -> Dict[str, str]:
        
        topic_schema = {}

        for column in df.columns:

            col_lower = column.lower()

            # Temporal data - anything related to time
            # 'any()' returns True if ANY word matches
            # Example: "birth_date", "created_time", "year_joined" → 'temporal'
            if any(word in col_lower for word in ['date', 'time', 'year']):
                topic_schema[column] = 'temporal'
            
            # Financial data - money-related columns
            # Example: "product_price", "total_cost", "salary_amount" → 'financial'
            elif any(word in col_lower for word in ['price', 'cost', 'amount', 'revenue', 'salary']):
                topic_schema[column] = 'financial'
            
            # Text data - descriptive fields
            # Example: "customer_name", "product_title", "job_description" → 'text'
            elif any(word in col_lower for word in ['name', 'title', 'description']):
                topic_schema[column] = 'text'
            
            # Identifiers - unique codes or numbers
            # Example: "user_id", "product_code", "order_number" → 'identifier'
            elif any(word in col_lower for word in ['id', 'code', 'number']):
                topic_schema[column] = 'identifier'
            
            # ===========================================================
            # TYPE-BASED DETECTION - Check actual data types
            # ===========================================================
            
            # Numeric data - integers or floats
            # pd.api.types.is_numeric_dtype() checks if the column contains numbers
            # Example: column with values [1, 2, 3, 4.5] → 'numeric'
            elif pd.api.types.is_numeric_dtype(df[column]):
                topic_schema[column] = 'numeric'
            
            # ===========================================================
            # DEFAULT CASE - Fallback category
            # ===========================================================
            
            # If none of the above match, assume it's categorical data
            # Categorical = limited set of values (like "Red", "Blue", "Green")
            # Example: "status", "category", "gender" → 'categorical'
            else:
                topic_schema[column] = 'categorical'

        return topic_schema
