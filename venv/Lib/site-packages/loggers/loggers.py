#!/usr/bin/python
import logging
import logging.handlers
import sys
import os

class Loggers(object):
    '''Provides log functionalities either in stream or file form

        Arguments:
            log_name (:obj:`str`): name of the log handler
            log_folder_path (:obj:`str`,optional, *default* =None):
             folder where the log's files will lie
            log_file (:obj:`str`,optional, *default* =None): path of
             the debug and error log's files
            logger (:obj:`obj`,optional, *default* =None): use this preexistent logger
             instead of creating a new one

    '''
    def __init__(self, log_name, **kwargs):
        default_args = {'log_folder_path': None, 'log_file': None, 'logger': None}
        default_args.update(kwargs)
        self.log = default_args['logger'] if default_args['logger'] else logging.getLogger(log_name)
        self.default_formatter = logging.Formatter('Log: %(message)s | Log level:%(levelname)s |\
                                 Date:%(asctime)s', datefmt='%d/%m/%Y %H:%M:%S')
        if not len(self.log.handlers):
            self.default_formatter = logging.Formatter(
                'Log: %(message)s | Log level:%(levelname)s | Date:%(asctime)s',
                datefmt='%d/%m/%Y %H:%M:%S')
            self.stream_handler = logging.StreamHandler(sys.stdout)
            self.stream_handler.setLevel(logging.DEBUG)
            self.stream_handler.setFormatter(self.default_formatter)
            self.log.addHandler(self.stream_handler)
        if default_args['log_folder_path']:
            log_name = default_args['log_file'] if default_args['log_file'] else log_name
            self.error_logfile = default_args['log_folder_path']+"/"+log_name+".error.log.bz2"
            self.debug_logfile = default_args['log_folder_path']+"/"+log_name+".debug.log.bz2"
            if not os.path.isdir(default_args['log_folder_path']):
                try:
                    os.mkdir(default_args['log_folder_path'])
                except Exception as error:
                    print ('It was not possible to write to the log folder ' +
                           default_args['log_folder_path']+'. You must create it\
                           manually and set the required permissions. Error: '+str(error))
            else:
                try:
                    self.debug_handler = logging.handlers.RotatingFileHandler(self.debug_logfile,
                                                                              maxBytes=600000,
                                                                              encoding='bz2-codec',
                                                                              backupCount=4)
                    self.error_handler = logging.handlers.RotatingFileHandler(self.error_logfile,
                                                                              maxBytes=600000,
                                                                              encoding='bz2-codec',
                                                                              backupCount=4)
                    self.debug_handler.setLevel(logging.DEBUG)
                    self.debug_handler.setFormatter(self.default_formatter)
                    self.error_handler.setLevel(logging.ERROR)
                    self.error_handler.setFormatter(self.default_formatter)
                except Exception as error:
                    print ('It was not possible to write to the log folder ' +
                           default_args['log_folder_path']+'. You must create it\
                           manually and set the required permissions. Error: '+str(error))

    def set_log_rotate_handler(self, set_file):
        '''Enables/disables logs to be written to files

        Arguments:
            set_file (:obj:`bool`): False disables, True enables

        '''
        if hasattr(self, 'debug_handler'):
            if set_file:
                self.log.addHandler(self.debug_handler)
                self.log.addHandler(self.error_handler)
            else:
                try:
                    self.log.removeHandler(self.error_handler)
                    self.log.removeHandler(self.debug_handler)
                except Exception:
                    pass
        else:
            self.log.debug('The file log handlers were not created. It is not\
                           possible to write to the log files.')

    def set_log_level(self, log_level):
        '''Configures class log level

        Arguments:
            log_level (:obj:`str`): log level ('NOTSET','DEBUG','INFO' 'WARNING',
                'ERROR', 'CRITICAL')

        '''
        if log_level == 'DEBUG':
            self.log.setLevel(logging.DEBUG)
            self.log.debug("Changing log level to "+log_level)
        elif log_level == 'INFO':
            self.log.setLevel(logging.INFO)
            self.log.info("Changing log level to "+log_level)
        elif log_level == 'WARNING':
            self.log.setLevel(logging.WARNING)
            self.log.warning("Changing log level to "+log_level)
        elif log_level == 'ERROR':
            self.log.setLevel(logging.ERROR)
            self.log.error("Changing log level to "+log_level)
        elif log_level == 'CRITICAL':
            self.log.setLevel(logging.CRITICAL)
            self.log.critical("Changing log level to "+log_level)
        elif log_level == 'NOTSET':
            self.log.setLevel(logging.NOTSET)
        else:
            raise NotImplementedError('Not implemented log level '+str(log_level))

    def set_log_format(self, log_type, log_format):
        '''Configures log format

        Arguments:
            log_type (:obj:`str`): log type (error, debug or stream)
            log_format (:obj:`str`): log format (ex:"Log: %(message)s | Log level:%(levelname)s |
                Date:%(asctime)s',datefmt='%m/%d/%Y %I:%M:%S")

        '''
        if not (log_type == 'error' or log_type == 'stream' or log_type == 'debug'):
            self.log.debug('Log type must be error, stream, or debug')
        else:
            self.default_formatter = logging.Formatter(log_format)
            if log_type == 'error':
                self.error_handler.setFormatter(self.default_formatter)
            elif log_type == 'debug':
                self.debug_handler.setFormatter(self.default_formatter)
            elif log_type == 'stream':
                self.stream_handler.setFormatter(self.default_formatter)

