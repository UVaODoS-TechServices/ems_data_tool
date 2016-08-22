#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Database handler for EMS Data Tool. """

import sys

from contextlib import contextmanager

import pyodbc

class PendingTransaction(Exception):
    def __init__(self, err_args):
        super(Exception, self).__init__("There are pending transactions".format(err_args or 0))

class DBHandler(object):
    """ Acts as handler for queries and transactions. """
    
    _conn = None
    _cur = None
    _trns_depth = 0
    
    @staticmethod
    def create_connmsg(server, driver, database, username, password, trusted):
        """ Creates a string that can be used to connect to an odbc database. """
        
        connmsg = ("SERVER={server};DRIVER={driver};DATABASE={database};"
                   "UID={username};PWD={password};Trusted_Connection={trusted};")
        
        return connmsg.format(server=server, driver=driver, database=database, \
                              username=username, password=password, \
                              trusted=trusted)
    
    @classmethod
    def pending(cls):
        """ Returns the current transaction depth. """
        
        return cls._trns_depth
    
    @classmethod
    def connect(cls, connmsg):
        """
            Connects the handler to the source specified by the connmsg.
            Returns True on success, error on failure.
        """
        
        try:
            cls._conn = pyodbc.connect(connmsg)
            cls._cur = cls._conn.cursor()
            return True
        
        except Exception, err:
            return err
    
    @classmethod
    def connected(cls):
        """ Checks to see if specified handler object is connected. """
        
        if cls._conn is not None:
            return True
        
        return False
    
    @classmethod
    def begin(cls):
        """ Starts a new transaction. """
        
        if not cls.connected():
            return False
        
        cls._cur.execute("BEGIN TRANSACTION")
        cls._trns_depth += 1
    
    @classmethod
    def end(cls):
        """ Commits pending transaction. """
        
        if not cls.connected():
            return False
        
        try:
            if cls._trns_depth > 0:
                cls._cur.commit()
                cls._trns_depth -= 1
        
        except Exception, err:
            return err
    
    @classmethod
    def commit_all(cls):
        """ Commits all pending transactions. """
        
        if not cls.connected():
            return False
        
        while cls._trns_depth > 0:
            try:
                cls._cur.commit()
                cls._trns_depth -= 1
            
            except Exception, err:
                return err
    
    @classmethod
    def rollback(cls):
        """ Rolls db state back to start of pending transaction. """
        
        if not cls.connected():
            return False
        
        if cls._trns_depth > 0:
            cls._cur.rollback()
            cls._trns_depth -= 1
    
    @classmethod
    def execute(cls, query, *args):
        """ Executes query with optional args. """
        
        if not cls.connected():
            return False
        
        try:
            cls._cur.execute(query, *args)
        
        except Exception, err:
            return err
    
    @classmethod
    def disconnect(cls, force=False):
        """
            Disconnects the handler from the data source.
            If there are pending transactions 'PendingTransactions'
            will be raised. 
            If 'force' is set to True it will rollback pending
            transactions and disconnect.
         """
        
        if (cls._trns_depth > 0) and not force:
            raise PendingTransaction(cls._trns_depth)
        
        elif force:
            while cls._trns_depth > 0:
                cls._cur.rollback()
        
        while cls.connected():
            cls._cur.close()
            cls._conn.close()
        
        cls._cur = None
        cls._conn = None
    
    @classmethod
    def get_result(cls):
        """ Returns result of last query. """
        
        if not cls.connected():
            return False
        
        return cls._cur.fetchall()


@contextmanager
def database(srv, drv, db, un, pw, tc):
    connmsg = "SERVER=%s;DRIVER=%s;DATABASE=%s;UID=%s;PWD=%s;"
    connmsg += "Trusted_Connect=%s;"
    connmsg = connmsg % (srv, drv, db, un, pw, tc,)
    
    def inner(*args, **kwargs):
        conn = pyodbc.connect(connmsg)
        cur = conn.cursor()
        
        return (conn, cur,)
    
    return inner


if __name__ == "__main__":
    pass
