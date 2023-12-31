#ifndef XSTRIGGERINDICATIONDATA_H
#define XSTRIGGERINDICATIONDATA_H

#include "xstypesconfig.h"
#include "pstdint.h"

#ifdef __cplusplus
extern "C" {
#endif
#ifndef __cplusplus
#define XSTRIGGERINDICATIONDATA_INITIALIZER	{ 0, 0, 0, 0 }
#endif

struct XsTriggerIndicationData;

XSTYPES_DLL_API void XsTriggerIndicationData_destruct(struct XsTriggerIndicationData* thisPtr);
XSTYPES_DLL_API int XsTriggerIndicationData_valid(const struct XsTriggerIndicationData* thisPtr);

#ifdef __cplusplus
} // extern "C"
#endif


/*! \brief Data for a trigger indication message */
struct XsTriggerIndicationData
{
	uint8_t m_line;			//!< The line number
	uint8_t m_polarity;		//!< The polarity
	uint32_t m_timestamp;	//!< The timestamp
	uint16_t m_frameNumber;	//!< The frame number

#ifdef __cplusplus
	/*! Constructor
		\param[in] line Line
		\param[in] polarity Polarity
		\param[in] timestamp Timestamp
		\param[in] frameNumber Frame number
	*/
	explicit XsTriggerIndicationData(uint8_t line = 0, uint8_t polarity = 0, uint32_t timestamp = 0, uint16_t frameNumber = 0)
		: m_line(line), m_polarity(polarity), m_timestamp(timestamp), m_frameNumber(frameNumber)
	{}

	/*! \brief \copybrief XsTriggerIndicationData_destruct */
	inline void clear()
	{
		XsTriggerIndicationData_destruct(this);
	}

	/*! \brief \copybrief XsTriggerIndicationData_valid */
	inline bool valid() const
	{
		return 0 != XsTriggerIndicationData_valid(this);
	}

	/*! \brief Returns true if all fields of this and \a other are exactly identical */
	inline bool operator == (XsTriggerIndicationData const& other) const
	{
		return m_line == other.m_line &&
			m_polarity == other.m_polarity &&
			m_timestamp == other.m_timestamp &&
			m_frameNumber == other.m_frameNumber;
	}
#endif
};

typedef struct XsTriggerIndicationData XsTriggerIndicationData;

#endif
