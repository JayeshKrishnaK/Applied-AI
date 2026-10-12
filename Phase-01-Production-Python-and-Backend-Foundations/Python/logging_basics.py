import logging

def main():
    creating_own_logger()

def creating_own_logger():
    # Uses root logger
    logging.info("I'm an info")

    # gets the logger object for root and its name is root
    root_logger = logging.getLogger()

    # creating a logger and its name is logging_basics and store that object in logger variable
    '''
    common convention which creates logger on the name of the module:
    logging.getLogger(__name__)
    '''
    logger = logging.getLogger("logging_basics")

    #Setting its own logger level
    logger.setLevel(logging.INFO)

    # Creating file handler and its own formatter
    file_handler = logging.FileHandler("logging_basics.log",mode="w")
    file_handler_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    file_handler.setFormatter(file_handler_formatter)
    file_handler.level = logging.WARN

    # creating console handler and its own formatter
    console_handler = logging.StreamHandler()
    console_handler_formatter = logging.Formatter("%(name)s %(levelname)s %(message)s")
    console_handler.setFormatter(console_handler_formatter)
    console_handler.level = logging.ERROR

    # Adding the handlers to my logger logging_basics
    # IMP: can't pass it as a list. addHandler accepts only one single object.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Here both objcts are present in handlers list attribute of 
    # logger object and the handlers we created are same.
    # addHandler receives the list and assignes it to this attribute
    print(logger.handlers,file_handler,console_handler)

    # Here both objcts are same. setFormatter receives the formatter object
    # and sets it to attribute formatter of handler object
    print(file_handler.formatter,file_handler_formatter)

    '''
    Instead of calling addhandler/setFormatter/setLevel we can directly assign them as:
    logger.handlers = [handler]
    logger.level = logging.INFO
    handler.formatter = formatter
    '''
    
    #Logging a message
    logger.info("This is INFO")
    logger.warning("This is WARN") # warn function is deprecated
    logger.error("This is ERROR")
    '''
    1. It's outputed both to console and file and each will have their own format of messaging and
       log levels
    2. WARNINGS will go to file and ERRORS will be printed in console as each handler has their own logging levels

    '''

    # Creatiing another logger w/o its own handler
    logger_two = logging.getLogger("logging_basics_2")
    logger_two.info("This is logger 2")

    '''
    1. Here its uses the handler,formatter,log levels used by the root handler.
    2. if root handler also has nothing configured. ie., just logging.basicConfig()
        default handler - console
        default format = %(levelname)s:%(name)s:%(message)s
        default level = WARNING (30) 
    '''

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename="log.log",
                        filemode="w",
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    print(logging.DEBUG) # 10
    main()