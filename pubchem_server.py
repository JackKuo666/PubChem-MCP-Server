from typing import Any, List, Dict, Optional
import asyncio
import logging
import pubchempy as pcp

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastMCP server
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("pubchem")

def compound_to_dict(compound):
    """Convert a PubChem compound to a dictionary with relevant information."""
    if not compound:
        return {}
    
    result = {
        "cid": compound.cid,
        "iupac_name": compound.iupac_name,
        "molecular_formula": compound.molecular_formula,
        "molecular_weight": compound.molecular_weight,
        "canonical_smiles": compound.canonical_smiles,
        "isomeric_smiles": compound.isomeric_smiles,
        "inchi": compound.inchi,
        "inchikey": compound.inchikey,
        "xlogp": compound.xlogp,
        "exact_mass": compound.exact_mass,
        "monoisotopic_mass": compound.monoisotopic_mass,
        "tpsa": compound.tpsa,
        "complexity": compound.complexity,
        "charge": compound.charge,
        "h_bond_donor_count": compound.h_bond_donor_count,
        "h_bond_acceptor_count": compound.h_bond_acceptor_count,
        "rotatable_bond_count": compound.rotatable_bond_count,
        "heavy_atom_count": compound.heavy_atom_count,
        "atom_stereo_count": compound.atom_stereo_count,
        "defined_atom_stereo_count": compound.defined_atom_stereo_count,
        "undefined_atom_stereo_count": compound.undefined_atom_stereo_count,
        "bond_stereo_count": compound.bond_stereo_count,
        "defined_bond_stereo_count": compound.defined_bond_stereo_count,
        "undefined_bond_stereo_count": compound.undefined_bond_stereo_count,
        "covalent_unit_count": compound.covalent_unit_count,
    }
    
    # Add synonyms if available
    if hasattr(compound, 'synonyms') and compound.synonyms:
        result["synonyms"] = compound.synonyms
    
    return result

def search_by_name(name: str, max_results: int = 5):
    """Search compounds by name."""
    try:
        compounds = pcp.get_compounds(name, 'name', record_type='3d', max_records=max_results)
        return [compound_to_dict(compound) for compound in compounds]
    except Exception as e:
        logging.error(f"Error searching by name '{name}': {str(e)}")
        return [{"error": f"An error occurred while searching: {str(e)}"}]

def search_by_smiles(smiles: str, max_results: int = 5):
    """Search compounds by SMILES."""
    try:
        compounds = pcp.get_compounds(smiles, 'smiles', record_type='3d', max_records=max_results)
        return [compound_to_dict(compound) for compound in compounds]
    except Exception as e:
        logging.error(f"Error searching by SMILES '{smiles}': {str(e)}")
        return [{"error": f"An error occurred while searching: {str(e)}"}]

def search_by_cid(cid: int):
    """Get compound by CID."""
    try:
        compound = pcp.Compound.from_cid(cid)
        return compound_to_dict(compound)
    except Exception as e:
        logging.error(f"Error fetching compound with CID {cid}: {str(e)}")
        return {"error": f"An error occurred while fetching compound: {str(e)}"}

@mcp.tool()
async def search_pubchem_by_name(name: str, max_results: int = 5) -> List[Dict[str, Any]]:
    logging.info(f"Searching for compounds with name: {name}, max_results: {max_results}")
    """
    Search for chemical compounds on PubChem using a compound name.

    Args:
        name: Name of the chemical compound
        max_results: Maximum number of results to return (default: 5)

    Returns:
        List of dictionaries containing compound information
    """
    try:
        results = await asyncio.to_thread(search_by_name, name, max_results)
        return results
    except Exception as e:
        return [{"error": f"An error occurred while searching: {str(e)}"}]

@mcp.tool()
async def search_pubchem_by_smiles(smiles: str, max_results: int = 5) -> List[Dict[str, Any]]:
    logging.info(f"Searching for compounds with SMILES: {smiles}, max_results: {max_results}")
    """
    Search for chemical compounds on PubChem using a SMILES string.

    Args:
        smiles: SMILES notation of the chemical compound
        max_results: Maximum number of results to return (default: 5)

    Returns:
        List of dictionaries containing compound information
    """
    try:
        results = await asyncio.to_thread(search_by_smiles, smiles, max_results)
        return results
    except Exception as e:
        return [{"error": f"An error occurred while searching: {str(e)}"}]

@mcp.tool()
async def get_pubchem_compound_by_cid(cid: int) -> Dict[str, Any]:
    logging.info(f"Fetching compound with CID: {cid}")
    """
    Fetch detailed information about a chemical compound using its PubChem CID.

    Args:
        cid: PubChem Compound ID (CID)

    Returns:
        Dictionary containing compound information
    """
    try:
        result = await asyncio.to_thread(search_by_cid, cid)
        return result
    except Exception as e:
        return {"error": f"An error occurred while fetching compound: {str(e)}"}

@mcp.tool()
async def search_pubchem_advanced(
    name: Optional[str] = None,
    smiles: Optional[str] = None,
    formula: Optional[str] = None,
    cid: Optional[int] = None,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    logging.info(f"Performing advanced search with parameters: {locals()}")
    """
    Perform an advanced search for compounds on PubChem.

    Args:
        name: Name of the chemical compound
        smiles: SMILES notation of the chemical compound
        formula: Molecular formula
        cid: PubChem Compound ID
        max_results: Maximum number of results to return (default: 5)

    Returns:
        List of dictionaries containing compound information
    """
    try:
        if cid is not None:
            result = await asyncio.to_thread(search_by_cid, cid)
            return [result]
        elif smiles is not None:
            return await asyncio.to_thread(search_by_smiles, smiles, max_results)
        elif name is not None:
            return await asyncio.to_thread(search_by_name, name, max_results)
        elif formula is not None:
            compounds = await asyncio.to_thread(pcp.get_compounds, formula, 'formula', max_records=max_results)
            return [compound_to_dict(compound) for compound in compounds]
        else:
            return [{"error": "At least one search parameter (name, smiles, formula, or cid) must be provided"}]
    except Exception as e:
        return [{"error": f"An error occurred while performing advanced search: {str(e)}"}]

if __name__ == "__main__":
    logging.info("Starting PubChem MCP server")
    # Initialize and run the server
    mcp.run(transport='stdio')
