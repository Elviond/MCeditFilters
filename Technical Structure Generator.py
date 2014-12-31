# This filter generates a bounding box of an abstract structure according to the selection box.

# This filter was written by Elviond.

# Feel free to modify this filter as long as you give credit to everyone involved.

# Instructions:
#
# Selection box:
# The selection box can be any size.
#
# Options info:
#
# Structure:
# The structure whose bounding box should fill the selection box.

from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String
from pymclevel import TAG_Long
from pymclevel import TAG_Float
from pymclevel import TAG_Byte_Array
from pymclevel import TAG_Int_Array
from pymclevel import load
from numpy import array
import os

displayName = "Technical structure generator 1.0"

inputs = (
	("Structure", ("Temple (witch hut)", "Nether fortress", "Ocean monument")),
	("Filter by Elviond", "label"),
)

def perform(level, box, options):
	
	# Convert input to feature and child id's.
	feature_ids = {
		"Temple (witch hut)": ("Temple", "TeSH"),
		"Nether fortress": ("Fortress", "NeBCr"),
		"Ocean monument": ("Monument", "OMB"),
	}
	
	(feature_id, feature_child_id) = feature_ids[options["Structure"]]
	
	coords = (box.minx, box.miny, box.minz, box.maxx, box.maxy, box.maxz)
	BB = TAG_Int_Array(array(coords))
	
	# Feature specifications.
	
	feature = TAG_Compound()
	feature["id"] = TAG_String(feature_id)
	feature["BB"] = BB
	feature["ChunkX"] = TAG_Int(box.minx/16)
	feature["ChunkZ"] = TAG_Int(box.minz/16)
	
	child = TAG_Compound()
	child["id"] = TAG_String(feature_child_id)
	child["BB"] = BB
		
	feature["Children"] = TAG_List([child])
	
	# For monuments: prevent physical structure generation
	
	if feature_id == "Monument":
		monx = box.minx/16
		monz = box.minz/16
		
		feature["Processed"] = TAG_List()
		
		for x in xrange(-2, 3):
			for z in xrange(-2, 3):
				processed_chunk = TAG_Compound()
				processed_chunk["X"] = TAG_Int(monx + x)
				processed_chunk["Z"] = TAG_Int(monz + z)
				
				feature["Processed"].append(processed_chunk)
			
	
	# Find structure file if it exists, if not, create a new one.
	if level.dimNo == 0:
		path = level.worldFolder.getFolderPath("data")
	else:
		path = level.parentWorld.worldFolder.getFolderPath("data")
	
	if feature_id + ".dat" in os.listdir(path):
		path += "/" + feature_id + ".dat"
		structure = load(path)
	else:
		path += "/" + feature_id + ".dat"
		structure = TAG_Compound()
		structure["data"] = TAG_Compound()
		structure["data"]["Features"] = TAG_Compound()
	
	# Name the feature generated.
	feature_name = "[" + str(box.minx/16) + ", " + str(box.minz/16) + "]"
	
	# Export the feature and save the structure.
	structure["data"]["Features"][feature_name] = feature
	structure.save(path)
