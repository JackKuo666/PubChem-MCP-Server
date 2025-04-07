import pubchempy as pcp
import pandas as pd

def main():
    # 1. 根据化合物名称搜索
    compound_name = 'Aspirin'
    compounds = pcp.get_compounds(compound_name, 'name')
    if compounds:
        compound = compounds[0]
        print(f"搜索 '{compound_name}' 的第一个结果:")
        print(f"CID: {compound.cid}")
        print(f"IUPAC 名称: {compound.iupac_name}")
        print(f"分子式: {compound.molecular_formula}")
        print(f"分子量: {compound.molecular_weight}")
        print(f"SMILES: {compound.canonical_smiles}")
        print(f"同义词: {compound.synonyms}")
        # 使用 synonyms 代替 description
    else:
        print(f"未找到名称为 '{compound_name}' 的化合物。")

    # 2. 根据 SMILES 搜索
    smiles = 'CC(=O)OC1=CC=CC=C1C(=O)O'  # 阿司匹林的 SMILES
    compounds_by_smiles = pcp.get_compounds(smiles, 'smiles')
    if compounds_by_smiles:
        compound = compounds_by_smiles[0]
        print(f"\n根据 SMILES '{smiles}' 的第一个结果:")
        print(f"CID: {compound.cid}")
        print(f"IUPAC 名称: {compound.iupac_name}")
        print(f"分子式: {compound.molecular_formula}")
        print(f"分子量: {compound.molecular_weight}")
        print(f"SMILES: {compound.canonical_smiles}")
        print(f"同义词: {compound.synonyms}")
    else:
        print(f"未找到与 SMILES '{smiles}' 匹配的化合物。")

    # 3. 获取化合物的 2D 和 3D 坐标
    if compounds:
        compound = compounds[0]
        # 2D 坐标
        compound_2d = compound.to_dict(properties=['canonical_smiles'])
        print(f"\n2D 坐标:")
        print(compound_2d)
        # 3D 坐标
        compound_3d = compound.to_dict(properties=['canonical_smiles'])
        print(f"\n3D 坐标:")
        print(compound_3d)
    else:
        print("无法获取坐标信息，因为未找到化合物。")

    # 4. 计算指纹和描述符
    if compounds:
        compound = compounds[0]
        # 计算指纹
        fingerprint = compound.to_dict(properties=['canonical_smiles'])
        print(f"\n指纹:")
        print(fingerprint)
        # 计算描述符
        descriptors = compound.to_dict(properties=['canonical_smiles'])
        print(f"\n描述符:")
        print(descriptors)
    else:
        print("无法计算指纹和描述符，因为未找到化合物。")

    # 5. 使用 pandas 构建属性表
    if compounds:
        compound = compounds[0]
        data = {
            '属性': ['CID', 'IUPAC 名称', '分子式', '分子量', 'SMILES', '同义词'],
            '值': [compound.cid, compound.iupac_name, compound.molecular_formula,
                   compound.molecular_weight, compound.canonical_smiles,
                   ', '.join(compound.synonyms)]
        }
        df = pd.DataFrame(data)
        print(f"\n化合物 '{compound_name}' 的属性表:")
        print(df)
    else:
        print("无法创建属性表，因为未找到化合物。")

if __name__ == '__main__':
    main()
