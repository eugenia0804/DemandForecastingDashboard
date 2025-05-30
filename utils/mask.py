import pandas as pd

# Read the original dataset from CSV
input_file = '#' # 'path/to/your/original_sales_df.csv'
output_file = 'masked_sales_df.csv'

df = pd.read_csv(input_file)
df = df.drop(columns=['Unnamed: 0'])

# Step 1: Mask PRODUCT codes
product_map = {prod: f'PRODUCT_{i+1}' for i, prod in enumerate(df['PRODUCT'].unique())}
df['PRODUCT'] = df['PRODUCT'].map(product_map)

# Step 2: Mask PROD_CAT
prod_cat_map = {cat: f'CAT_{i+1}' for i, cat in enumerate(df['PROD_CAT'].unique())}
df['PROD_CAT'] = df['PROD_CAT'].map(prod_cat_map)

# Step 3: Mask PROD_DESCRIPTION based on PROD_CAT
df['PRODUCT_DESCRIPTION'] = df['PROD_CAT'].apply(lambda cat: f'{cat}_DES')

# For SHIP_VIA_TYPE map all non NA value that is not equals to WILL CALL to UPS GROUND
df['SHIP_VIA_TYPE'] = df['SHIP_VIA_TYPE'].str.strip()
ship_via_map = {ship: 'UPS GROUND' for ship in df['SHIP_VIA_TYPE'].unique() if pd.notna(ship) and ship != 'WILL CALL'}
df['SHIP_VIA_TYPE'] = df['SHIP_VIA_TYPE'].map(ship_via_map).fillna('WILL CALL')

df.reset_index(drop=True, inplace=True)
df.to_csv(output_file, index=False)
print(f"Masked dataset saved to '{output_file}'")
