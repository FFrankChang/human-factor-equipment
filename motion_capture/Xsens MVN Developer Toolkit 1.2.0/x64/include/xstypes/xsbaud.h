#ifndef XSBAUD_H
#define XSBAUD_H

#include "xstypesconfig.h"


/*!	\addtogroup enums Global enumerations
	@{
*/

#include "xsbaudcode.h"
#include "xsbaudrate.h"

/*! @} */

typedef enum XsBaudCode XsBaudCode;
typedef enum XsBaudRate XsBaudRate;

#ifdef __cplusplus
extern "C" {
#endif

XSTYPES_DLL_API XsBaudRate XsBaud_codeToRate(XsBaudCode baudcode);
XSTYPES_DLL_API XsBaudCode XsBaud_rateToCode(XsBaudRate baudrate);
XSTYPES_DLL_API int XsBaud_rateToNumeric(XsBaudRate baudrate);
XSTYPES_DLL_API XsBaudRate XsBaud_numericToRate(int numeric);

#ifdef __cplusplus
} // extern "C"

/*! \namespace XsBaud
	\brief Namespace for Baud rate and Baud code constants and conversions
*/
namespace XsBaud
{
/*! \copydoc XsBaud_codeToRate */
inline XsBaudRate codeToRate(XsBaudCode baudcode)
{
	return XsBaud_codeToRate(baudcode);
}
/*! \copydoc XsBaud_rateToCode */
inline XsBaudCode rateToCode(XsBaudRate baudrate)
{
	return XsBaud_rateToCode(baudrate);
}
/*! \copydoc XsBaud_rateToNumeric */
inline int rateToNumeric(XsBaudRate baudrate)
{
	return XsBaud_rateToNumeric(baudrate);
}
/*! \copydoc XsBaud_numericToRate*/
inline XsBaudRate numericToRate(int numeric)
{
	return XsBaud_numericToRate(numeric);
}
}

#ifndef XSENS_NO_STL
#include <ostream>

namespace std
{
/*! \brief Stream output operator for XsBaudRate */
template<typename _CharT, typename _Traits>
basic_ostream<_CharT, _Traits>& operator<<(basic_ostream<_CharT, _Traits>& o, XsBaudRate const& xd)
{
	return (o << XsBaud::rateToNumeric(xd));
}
}
#endif

#endif

#endif
