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
    node.addService(pg.Execute(shell='sh', command="""\
    echo "export MASTER_ADDR=10.10.1.1" > /local/repository/env.sh;
    echo "export MASTER_PORT=29500" >> /local/repository/env.sh;
    echo "export WORLD_SIZE={}" >> /local/repository/env.sh;
    echo "export RANK={}" >> /local/repository/env.sh;
    chmod +x /local/repository/env.sh;
    """.format(params.nodeCount, i)))
    node.addService(pg.Execute(shell='sh', command="source /local/repository/env.sh"))
    # command="""\
    # echo "MASTER_ADDR=10.10.1.1" | sudo tee -a /etc/environment;
    # echo "MASTER_PORT=29500" | sudo tee -a /etc/environment;
    # echo "WORLD_SIZE={}" | sudo tee -a /etc/environment;
    # echo "RANK={}" | sudo tee -a /etc/environment;
    # """.format(params.nodeCount, i)
    # node.addService(pg.Execute(shell='sh', command="export MASTER_ADDR=10.10.1.1 && export MASTER_PORT=29500 && export WORLD_SIZE={} && export RANK={} && env > /local/repository/env_log.txt".format(params.nodeCount, i)))
    # node.addService(pg.Execute(shell='sh', command="echo {} > /local/node_rank".format(i)))
    # node.addService(pg.Execute(shell='sh', command="echo {} > /local/node_count".format(params.nodeCount)))
    # node.addService(pg.Execute(shell='sh', command="chmod +x /local/repository/setup.sh"))
    # node.addService(pg.Execute(shell="sh", command="source /local/repository/setup.sh"))

# Output the request RSpec
pc.printRequestRSpec(request)
