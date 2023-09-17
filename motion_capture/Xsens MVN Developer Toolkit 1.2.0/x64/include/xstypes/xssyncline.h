#ifndef XSSYNCLINE_H
#define XSSYNCLINE_H

/*!	\addtogroup enums Global enumerations
	@{
*/

//AUTO namespace xstypes {
/*! \brief Synchronization line identifiers */
enum XsSyncLine
{
	XSL_Inputs,							/*!< \brief Value for checking if a line is an input, any item equal to or greater than XSL_Inputs and less than XSL_Outputs is an input */
	XSL_In1 = XSL_Inputs,				/*!< \brief Sync In 1 \remark Applies to Awinda Station and Mt */
	XSL_In2,							/*!< \brief Sync In 2 \remark Applies to Awinda Station */
	XSL_In3,							/*!< \brief Sync In 3 \remark Applies to MTi-680 */
	XSL_Bi1In,							/*!< \brief Bidirectional Sync 1 In */
	XSL_ClockIn,						/*!< \brief Clock synchronisation input \remark Applies to Mk4 */
	XSL_CtsIn,							/*!< \brief RS232 CTS sync in */
	XSL_GnssClockIn,					/*!< \brief Clock synchronisation input line attached to internal GNSS unit \remark Applies to Mk4 */
	XSL_ExtTimepulseIn,					/*!< \brief External time pulse input (e.g. for external GNSS unit) \remark Applies to Mk4 with external device */
	XSL_ReqData,						/*!< \brief Serial data sync option, use \a XMID_ReqData message id for this \remark Applies to Mk4*/
	XSL_Gnss1Pps,						/*!< \brief GNSS 1PPS pulse sync line \remark Applies to MTi-7*/

	XSL_Outputs,						/*!< \brief Value for checking if a line is output. Values equal to or greater than this are outputs */
	XSL_Out1 = XSL_Outputs,				/*!< \brief Sync Out 1 \remark Applies to Awinda Station and Mt */
	XSL_Out2,							/*!< \brief Sync Out 2 \remark Applies to Awinda Station */
	XSL_Bi1Out,							/*!< \brief Bidirectional Sync 1 Out */
	XSL_RtsOut,							/*!< \brief RS232 RTS sync out */

	XSL_Invalid							/*!< \brief Invalid sync setting. Used if no sync line is set */
};
/*! @} */
typedef enum XsSyncLine XsSyncLine;
//AUTO }

#endif
