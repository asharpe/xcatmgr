
class Cluster:
	def __init__(self, name="Cluster", mgmt_node=None):
		self.name = name
		self.mgmt_node = mgmt_node
		self.racks = []

	def addRack(self, rack):
		self.racks.append(rack)

	def size(self):
		return self.racks.length

	size = property(size)

