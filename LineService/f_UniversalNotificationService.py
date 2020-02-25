#
# Autogenerated by Frugal Compiler (3.7.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#



from threading import Lock

from frugal.middleware import Method
from frugal.exceptions import TApplicationExceptionType
from frugal.exceptions import TTransportExceptionType
from frugal.processor import FBaseProcessor
from frugal.processor import FProcessorFunction
from frugal.util.deprecate import deprecated
from frugal.util import make_hashable
from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
from thrift.transport.TTransport import TTransportException

from .ttypes import *


class Iface(object):

    def notify(self, ctx, event):
        """
        Args:
            ctx: FContext
            event: GlobalEvent
        """
        pass


class Client(Iface):

    def __init__(self, provider, middleware=None):
        """
        Create a new Client with an FServiceProvider containing a transport
        and protocol factory.

        Args:
            provider: FServiceProvider with TSynchronousTransport
            middleware: ServiceMiddleware or list of ServiceMiddleware
        """
        middleware = middleware or []
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]
        self._transport = provider.get_transport()
        self._protocol_factory = provider.get_protocol_factory()
        self._oprot = self._protocol_factory.get_protocol(self._transport)
        self._iprot = self._protocol_factory.get_protocol(self._transport)
        self._write_lock = Lock()
        middleware += provider.get_middleware()
        self._methods = {
            'notify': Method(self._notify, middleware),
        }

    def notify(self, ctx, event):
        """
        Args:
            ctx: FContext
            event: GlobalEvent
        """
        return self._methods['notify']([ctx, event])

    def _notify(self, ctx, event):
        self._send_notify(ctx, event)
        self._recv_notify(ctx)

    def _send_notify(self, ctx, event):
        oprot = self._oprot
        with self._write_lock:
            oprot.get_transport().set_timeout(ctx.timeout)
            oprot.write_request_headers(ctx)
            oprot.writeMessageBegin('notify', TMessageType.CALL, 0)
            args = notify_args()
            args.event = event
            args.write(oprot)
            oprot.writeMessageEnd()
            oprot.get_transport().flush()

    def _recv_notify(self, ctx):
        self._iprot.read_response_headers(ctx)
        _, mtype, _ = self._iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(self._iprot)
            self._iprot.readMessageEnd()
            if x.type == TApplicationExceptionType.RESPONSE_TOO_LARGE:
                raise TTransportException(type=TTransportExceptionType.RESPONSE_TOO_LARGE, message=x.message)
            raise x
        result = notify_result()
        result.read(self._iprot)
        self._iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

class Processor(FBaseProcessor):

    def __init__(self, handler, middleware=None):
        """
        Create a new Processor.

        Args:
            handler: Iface
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]

        super(Processor, self).__init__()
        self.add_to_processor_map('notify', _notify(Method(handler.notify, middleware), self.get_write_lock()))


class _notify(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_notify, self).__init__(handler, lock)

    def process(self, ctx, iprot, oprot):
        args = notify_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = notify_result()
        try:
            self._handler([ctx, args.event])
        except UniversalNotificationServiceException as e:
            result.e = e
        except TApplicationException as ex:
            with self._lock:
                _write_application_exception(ctx, oprot, "notify", exception=ex)
                return
        except Exception as e:
            with self._lock:
                _write_application_exception(ctx, oprot, "notify", ex_code=TApplicationExceptionType.INTERNAL_ERROR, message=e.message)
            raise
        with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('notify', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except TTransportException as e:
                # catch a request too large error because the TMemoryOutputBuffer always throws that if too much data is written
                if e.type == TTransportExceptionType.REQUEST_TOO_LARGE:
                    raise _write_application_exception(ctx, oprot, "notify", ex_code=TApplicationExceptionType.RESPONSE_TOO_LARGE, message=e.args[0])
                else:
                    raise e


def _write_application_exception(ctx, oprot, method, ex_code=None, message=None, exception=None):
    if exception is not None:
        x = exception
    else:
        x = TApplicationException(type=ex_code, message=message)
    oprot.write_response_headers(ctx)
    oprot.writeMessageBegin(method, TMessageType.EXCEPTION, 0)
    x.write(oprot)
    oprot.writeMessageEnd()
    oprot.get_transport().flush()
    return x

class notify_args(object):
    """
    Attributes:
     - event
    """
    def __init__(self, event=None):
        self.event = event

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 2:
                if ftype == TType.STRUCT:
                    self.event = GlobalEvent()
                    self.event.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('notify_args')
        if self.event is not None:
            oprot.writeFieldBegin('event', TType.STRUCT, 2)
            self.event.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.event))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class notify_result(object):
    """
    Attributes:
     - e
    """
    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.e = UniversalNotificationServiceException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('notify_result')
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.e))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

