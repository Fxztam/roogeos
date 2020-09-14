import logging,sys

m_log_plsql = False
m_log_plsql_first = True

m_loginit = None

# file logging
def flog(p_msg, p_file="./flog", p_ext='log'):
    if p_file != "./flog":
        fo = open("./flog-" + p_file + "." + p_ext, "w")
    else:
        fo = open(p_file + "." + p_ext, "w")
    fo.write(p_msg + "\n")
    fo.close()
    return

# the same as flog but write append !
def floga(p_msg, p_file="./flog", p_ext='log'):
    if p_file != "./flog":
        fo = open("./flog-" + p_file + "." + p_ext, "a")
    else:
        fo = open(p_file + "." + p_ext, "a")
    fo.write(p_msg + "\n")
    fo.close()
    return

def chk4init():
    global m_loginit
    if m_loginit is None:
        print('--- Init Logging ---')
        init_logging('')
    return

# format='%(asctime)s - %(message)s', level=logging.INFO
def init_logging(p_msg):
    global m_loginit
    if m_loginit is None:
        logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        #logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        # console handling !
        console = logging.StreamHandler(sys.stdout)
        # optional, set the logging level
        console.setLevel(logging.INFO)
        # set a format which is the same for console use
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
        logging.info(p_msg)
        m_loginit = 'INIT'
    return

def loginfo(p_msg):
    chk4init()
    logging.info(p_msg)

def logwarn(p_msg):
    chk4init()
    logging.warning(p_msg)

def logdeb(p_msg):
    chk4init()
    logging.debug(p_msg)

def logerr(p_msg):
    chk4init()
    logging.error(p_msg)

def logcrit(p_msg):
    chk4init()
    logging.critical(p_msg)

def logexcep(p_msg):
    chk4init()
    logging.exception(p_msg)

if __name__ == '__init__':
    print("§§§§§§§§§")
    m_loginit = None
