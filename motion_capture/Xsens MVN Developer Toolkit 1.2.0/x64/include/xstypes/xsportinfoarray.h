#ifndef XSPORTINFOARRAY_H
#define XSPORTINFOARRAY_H

#include "xsarray.h"
#include "xsportinfo.h"

#ifdef __cplusplus
extern "C" {
#endif

extern XsArrayDescriptor const XSTYPES_DLL_API g_xsPortInfoArrayDescriptor;

#ifndef __cplusplus
#define XSPORTINFOARRAY_INITIALIZER	XSARRAY_INITIALIZER(&g_xsPortInfoArrayDescriptor)
struct XsPortInfo;

XSARRAY_STRUCT(XsPortInfoArray, struct XsPortInfo);
typedef struct XsPortInfoArray XsPortInfoArray;

XSTYPES_DLL_API void XsPortInfoArray_construct(XsPortInfoArray* thisPtr, XsSize count, struct XsPortInfo const* src);
#endif

#ifdef __cplusplus
} // extern "C"

struct XsPortInfoArray : public XsArrayImpl<XsPortInfo, g_xsPortInfoArrayDescriptor, XsPortInfoArray>
{
	//! \brief Constructs an XsPortInfoArray
	inline explicit XsPortInfoArray(XsSize sz = 0, XsPortInfo const* src = 0)
		: ArrayImpl(sz, src)
	{
	}

	//! \brief Constructs an XsPortInfoArray as a copy of \a other
	inline XsPortInfoArray(XsPortInfoArray const& other)
		: ArrayImpl(other)
	{
	}

	//! \brief Constructs an XsPortInfoArray that references the data supplied in \a ref
	inline explicit XsPortInfoArray(XsPortInfo* ref, XsSize sz, XsDataFlags flags /* = XSDF_None */)
		: ArrayImpl(ref, sz, flags)
	{
	}

#ifndef SWIG
	/*! \brief Swap the contents the \a first and \a second array */
	friend void swap(XsPortInfoArray& first, XsPortInfoArray& second)
	{
		first.swap(second);
	}
#endif

#ifndef XSENS_NOITERATOR
	//! \brief Constructs an XsPortInfoArray with the array bound by the supplied iterators \a beginIt and \a endIt
	template <typename Iterator>
	inline XsPortInfoArray(Iterator beginIt, Iterator endIt)
		: ArrayImpl(beginIt, endIt)
	{
	}
#endif
};
#endif

#endif
