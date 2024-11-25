import geni.portal as portal
import geni.rspec.pg as pg

# Create a portal context and define parameters
pc = portal.Context()
pc.defineParameter("nodeCount", "Number of Nodes", portal.ParameterType.INTEGER, 1)
params = pc.bindParameters()

# Create a Request object
request = pc.makeRequestRSpec()

# Create nodes and set disk image
for i in range(params.nodeCount):
    node = request.RawPC("node" + str(i))
    node.disk_image = "urn:publicid:IDN+wisc.cloudlab.us+image+distribml-PG0:small-lan.node0"
    node.addService(pg.Execute(shell='sh', command="export MASTER_ADDR=10.10.1.1"))
    node.addService(pg.Execute(shell='sh', command="export MASTER_PORT=29500"))
    node.addService(pg.Execute(shell='sh', command="export WORLD_SIZE={}".format(params.nodeCount)))
    node.addService(pg.Execute(shell='sh', command="export RANK={}".format(i)))
    # node.addService(pg.Execute(shell='sh', command="echo {} > /local/node_rank".format(i)))
    # node.addService(pg.Execute(shell='sh', command="echo {} > /local/node_count".format(params.nodeCount)))
    # node.addService(pg.Execute(shell='sh', command="chmod +x /local/repository/setup.sh"))
    # node.addService(pg.Execute(shell="sh", command="source /local/repository/setup.sh"))

# Output the request RSpec
pc.printRequestRSpec(request)
