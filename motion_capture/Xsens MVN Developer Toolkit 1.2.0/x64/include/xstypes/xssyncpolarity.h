#ifndef XSSYNCPOLARITY_H
#define XSSYNCPOLARITY_H

/*!	\addtogroup enums Global enumerations
	@{
*/

//AUTO namespace xstypes {
/*! \brief Signal polarity */
enum XsSyncPolarity
{
	XSP_None = 0,						/*!< \brief Don't generate or react to trigger level changes */
	XSP_RisingEdge = 1,					/*!< \brief React to a rising edge on input */
	XSP_PositivePulse = XSP_RisingEdge,	/*!< \brief Generate a positive pulse on output */
	XSP_FallingEdge = 2,					/*!< \brief React to a falling edge on input */
	XSP_NegativePulse = XSP_FallingEdge,	/*!< \brief Generate a falling edge on output */
	XSP_Both							/*!< \brief Toggle output or react on all toggles on input */
};
/*! @} */
typedef enum XsSyncPolarity XsSyncPolarity;
//AUTO }

#endif
