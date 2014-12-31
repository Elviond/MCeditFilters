# This filter replaces every block but a certain one by a given block.

# This filter was written by Elviond.

# Feel free to modify this filter as long as you give credit to everyone involved.

# Instructions:
#
# Selection box:
# The selection box can be any size.
#
# Options info:
#
# Fill with:
# The block used to fill in the selection.
#
# Except for:
# The blocks which won't be replaced.
#
# Any data value:
# Any data value of the block above won't be replaced. If false, the filter will replace all versions of the block except for the one selected (this is part of the "Except for" option).

displayName = "Inverted Replacer 1.0"

inputs = (
	("Fill with", "blocktype"),
	("Except for", "blocktype"),
	("Any data value", True),
	("Filter by Elviond", "label"),
)

########## Fast data access ##########

def blockAt(x, y, z, level):
	chunk = level.getChunk(x/16, z/16)
	if chunk == None:
		return 0
	return chunk.Blocks[x%16][z%16][y]

def dataAt(x, y, z, level):
	chunk = level.getChunk(x/16, z/16)
	if chunk == None:
		return 0
	return chunk.Data[x%16][z%16][y]

########## End fast data access ##########

def perform(level, box, options):
	
	block1 = options["Fill with"]
	block2 = options["Except for"]
	any_data = options["Any data value"]
	
	for x in xrange(box.minx, box.maxx):
		for y in xrange(box.miny, box.maxy):
			for z in xrange(box.minz, box.maxz):
				if blockAt(x, y, z, level) == block2.ID and (any_data or dataAt(x, y, z, level) == block2.blockData):
					continue
				level.setBlockAt(x, y, z, block1.ID)
				level.setBlockDataAt(x, y, z, block1.blockData)
