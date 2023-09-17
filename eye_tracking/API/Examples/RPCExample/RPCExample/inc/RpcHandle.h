#pragma once

#include <SEJsonRpc.h>

class RpcHandle
{
  SEJsonRpcHandle m_handle;
  SEJsonRpcRequestResult m_initError;

public:
  explicit RpcHandle(const char* hostname = "127.0.0.1", int port = 8100) : m_handle(nullptr)
  {
    m_initError = seInitialize(&m_handle, hostname, port);
  }

  RpcHandle(const RpcHandle&) = delete;
  RpcHandle(RpcHandle&& other) = delete;
  RpcHandle& operator=(const RpcHandle&) = delete;
  RpcHandle& operator=(const RpcHandle&&) = delete;

  ~RpcHandle()
  {
    seFree(m_handle);
  }

  SEJsonRpcHandle get() const
  {
    return m_handle;
  }

  SEJsonRpcRequestResult initError() const
  {
    return m_initError;
  }
};
