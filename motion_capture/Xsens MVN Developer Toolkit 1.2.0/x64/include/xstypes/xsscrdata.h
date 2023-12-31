#ifndef XSSCRDATA_H
#define XSSCRDATA_H

#include "pstdint.h"
#include "xsushortvector.h"

#ifndef __cplusplus
	#define XSSCRDATA_INITIALIZER {XSUSHORTVECTOR_INITIALIZER, XSUSHORTVECTOR_INITIALIZER, XSUSHORTVECTOR_INITIALIZER, {0, 0, 0, 0}}
#endif

/*! \brief Container for raw sensor measurement data
	\details This structure contains raw measurement data from the sensors on the device.
	This data is unscaled, the bias has not been subtracted and no error correction has been applied.
*/
struct XsScrData
{
	XsUShortVector	m_acc;	//!< The raw accelerometer data
	XsUShortVector	m_gyr;	//!< The raw gyroscope data
	XsUShortVector	m_mag;	//!< The raw magnetometer data
	uint16_t		m_temp;	//!< The temperature data
};
typedef struct XsScrData XsScrData;

#endif
