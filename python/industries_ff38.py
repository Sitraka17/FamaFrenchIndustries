"""
********************************************************************************
Author:     SITRAKA FORLER (lux-aiops.com)
            Python translation based on original SAS code by:
            Ed deHaan, with Jess Blocker Smith, Xue Li, and unknown other authors
            Xue Li rechecked assignments on 3/24/2021

Purpose:    To assign Fama-French 38 industry codes based on 4-digit SIC codes

Version:    1.0 - Python translation - 10/26/2025

Notes:      38 Industry classification codes obtained from French's website
            http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
            
            Original SAS macro versions:
            1.0 - date? - original version
            1.1 - 03/24/21 - added classifications for SIC codes 900 (Fishing, 
                  Hunting and Trapping), 3990 (Miscellaneous Manufacturing 
                  Industries), and 6797 (Miscellaneous Investing)
********************************************************************************
"""

import pandas as pd
import numpy as np

# Fama-French 38 industry names (as per French's website)
FF38_NAMES = {
    1: 'Agric',   # Agriculture, forestry, and fishing
    2: 'Mines',   # Mining
    3: 'Oil',     # Oil and Gas Extraction
    4: 'Stone',   # Nonmetalic Minerals Except Fuels
    5: 'Cnstr',   # Construction
    6: 'Food',    # Food and Kindred Products
    7: 'Smoke',   # Tobacco Products
    8: 'Txtls',   # Textile Mill Products
    9: 'Apprl',   # Apparel and other Textile Products
    10: 'Wood',   # Lumber and Wood Products
    11: 'Chair',  # Furniture and Fixtures
    12: 'Paper',  # Paper and Allied Products
    13: 'Print',  # Printing and Publishing
    14: 'Chems',  # Chemicals and Allied Products
    15: 'Ptrlm',  # Petroleum and Coal Products
    16: 'Rubbr',  # Rubber and Miscellaneous Plastics Products
    17: 'Lethr',  # Leather and Leather Products
    18: 'Glass',  # Stone, Clay and Glass Products
    19: 'Metal',  # Primary Metal Industries
    20: 'MtlPr',  # Fabricated Metal Products
    21: 'Machn',  # Machinery, Except Electrical
    22: 'Elctr',  # Electrical and Electronic Equipment
    23: 'Cars',   # Transportation Equipment
    24: 'Instr',  # Instruments and Related Products
    25: 'Manuf',  # Miscellaneous Manufacturing Industries
    26: 'Trans',  # Transportation
    27: 'Phone',  # Telephone and Telegraph Communication
    28: 'TV',     # Radio and Television Broadcasting
    29: 'Utils',  # Electric, Gas, and Water Supply
    30: 'Garbg',  # Sanitary Services
    31: 'Steam',  # Steam Supply
    32: 'Water',  # Irrigation Systems
    33: 'Whlsl',  # Wholesale
    34: 'Rtail',  # Retail Stores
    35: 'Money',  # Finance, Insurance, and Real Estate
    36: 'Srvc',   # Services
    37: 'Govt',   # Public Administration
    38: 'Other',  # Almost Nothing
}

def assign_ff38_industry(df, sic_col='sic', prefix='i', ind_code_col='FF_IND_CODE'):
    """
    Assign Fama-French 38-industry codes to a DataFrame using SIC codes.
    
    Adds to the DataFrame:
        - ind_code_col: integer industry code (1-38)
        - 'FF_IND': textual industry name
        - 38 one-hot encoded columns (prefix1, prefix2, ..., prefix38)
    
    Parameters:
        df: pandas DataFrame with SIC codes
        sic_col: column name for SIC code (must be 4-digit integer or NaN)
        prefix: prefix for 38 binary columns ('i' → i1, i2, ..., i38)
        ind_code_col: name for industry code column
    
    Returns:
        df: pandas DataFrame with new columns added
    """
    df = df.copy()

    def get_ff38_code(sic):
        if pd.isnull(sic):
            return np.nan
        sic = int(sic)
        
        # 1 Agric: Agriculture, forestry, and fishing
        if 100 <= sic <= 999:
            return 1
        
        # 2 Mines: Mining
        if 1000 <= sic <= 1299:
            return 2
        
        # 3 Oil: Oil and Gas Extraction
        if 1300 <= sic <= 1399:
            return 3
        
        # 4 Stone: Nonmetalic Minerals Except Fuels
        if 1400 <= sic <= 1499:
            return 4
        
        # 5 Cnstr: Construction
        if 1500 <= sic <= 1799:
            return 5
        
        # 6 Food: Food and Kindred Products
        if 2000 <= sic <= 2099:
            return 6
        
        # 7 Smoke: Tobacco Products
        if 2100 <= sic <= 2199:
            return 7
        
        # 8 Txtls: Textile Mill Products
        if 2200 <= sic <= 2299:
            return 8
        
        # 9 Apprl: Apparel and other Textile Products
        if 2300 <= sic <= 2399:
            return 9
        
        # 10 Wood: Lumber and Wood Products
        if 2400 <= sic <= 2499:
            return 10
        
        # 11 Chair: Furniture and Fixtures
        if 2500 <= sic <= 2599:
            return 11
        
        # 12 Paper: Paper and Allied Products
        if 2600 <= sic <= 2661:
            return 12
        
        # 13 Print: Printing and Publishing
        if 2700 <= sic <= 2799:
            return 13
        
        # 14 Chems: Chemicals and Allied Products
        if 2800 <= sic <= 2899:
            return 14
        
        # 15 Ptrlm: Petroleum and Coal Products
        if 2900 <= sic <= 2999:
            return 15
        
        # 16 Rubbr: Rubber and Miscellaneous Plastics Products
        if 3000 <= sic <= 3099:
            return 16
        
        # 17 Lethr: Leather and Leather Products
        if 3100 <= sic <= 3199:
            return 17
        
        # 18 Glass: Stone, Clay and Glass Products
        if 3200 <= sic <= 3299:
            return 18
        
        # 19 Metal: Primary Metal Industries
        if 3300 <= sic <= 3399:
            return 19
        
        # 20 MtlPr: Fabricated Metal Products
        if 3400 <= sic <= 3499:
            return 20
        
        # 21 Machn: Machinery, Except Electrical
        if 3500 <= sic <= 3599:
            return 21
        
        # 22 Elctr: Electrical and Electronic Equipment
        if 3600 <= sic <= 3699:
            return 22
        
        # 23 Cars: Transportation Equipment
        if 3700 <= sic <= 3799:
            return 23
        
        # 24 Instr: Instruments and Related Products
        if 3800 <= sic <= 3879:
            return 24
        
        # 25 Manuf: Miscellaneous Manufacturing Industries
        if 3900 <= sic <= 3999:
            return 25
        
        # 26 Trans: Transportation
        if 4000 <= sic <= 4799:
            return 26
        
        # 27 Phone: Telephone and Telegraph Communication
        if 4800 <= sic <= 4829:
            return 27
        
        # 28 TV: Radio and Television Broadcasting
        if 4830 <= sic <= 4899:
            return 28
        
        # 29 Utils: Electric, Gas, and Water Supply
        if 4900 <= sic <= 4949:
            return 29
        
        # 30 Garbg: Sanitary Services
        if 4950 <= sic <= 4959:
            return 30
        
        # 31 Steam: Steam Supply
        if 4960 <= sic <= 4969:
            return 31
        
        # 32 Water: Irrigation Systems
        if 4970 <= sic <= 4979:
            return 32
        
        # 33 Whlsl: Wholesale
        if 5000 <= sic <= 5199:
            return 33
        
        # 34 Rtail: Retail Stores
        if 5200 <= sic <= 5999:
            return 34
        
        # 35 Money: Finance, Insurance, and Real Estate
        if 6000 <= sic <= 6999:
            return 35
        
        # 36 Srvc: Services
        if 7000 <= sic <= 8999:
            return 36
        
        # 37 Govt: Public Administration
        if 9000 <= sic <= 9999:
            return 37
        
        # 38 Other: Almost Nothing
        return 38
        
    # Assign industry code
    df[ind_code_col] = df[sic_col].apply(get_ff38_code)
    
    # Assign textual name
    df['FF_IND'] = df[ind_code_col].map(FF38_NAMES)

    # Add 38 binary columns (one-hot encoding)
    for i in range(1, 39):
        col = f'{prefix}{i}'
        df[col] = (df[ind_code_col] == i).astype(int)

    return df


# Example Usage:
if __name__ == "__main__":
    # Example DataFrame with various SIC codes
    df = pd.DataFrame({
        'sic': [900, 1311, 2050, 2834, 3571, 3990, 4820, 5001, 6021, 6797, 
                7372, 8001, 9100, None]
    })

    # Assign Fama-French codes
    df_ff38 = assign_ff38_industry(df, sic_col='sic', prefix='i', ind_code_col='FF_IND_CODE')

    # Display results (showing only key columns for readability)
    print(df_ff38[['sic', 'FF_IND_CODE', 'FF_IND', 'i1', 'i3', 'i6', 'i35', 'i36', 'i37', 'i38']])
    
    # To get list of all industry dummy columns (equivalent to global macro variable)
    industry_fe_columns = [f'i{i}' for i in range(1, 39)]
    print(f"\nIndustry FE columns: {' '.join(industry_fe_columns)}")
