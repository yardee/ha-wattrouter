/**************************************************************************
 * @file  : time_schedule_mode_flags.h 
 * @brief : Contains declarations for the mode field.
 * @version : 1.0
 * @date  : 25. Nov. 2021
 * @copyright: 2021 SOLAR controls s.r.o.
 *************************************************************************/

/*
  The mode field is a 32 bit unsigned integer. 
  It is a bit mask.
  If the field is used for the checkbox then the checkbox is checked when the corresponding bit is nonzero.
  */

// Time schedule mode:
#define dTIME_MODE_MASK 0x0000000F // time schedule mode mask (reserved for up to 15 modes)
// Possible values:
#define dTIME_MODE_UNUSED 0x00000000 // time schedule is not used
#define dTIME_MODE_RESTRICT 0x00000001 // time schedule restricts output activity to given time interval
#define dTIME_MODE_ENFORCE 0x00000002 // time schedule forces output activity to given time interval

// Time schedule conditions:
#define dTIME_COND_MASK 0x000000F0 // time schedule condition mask
// Possible fields:
#define dTIME_COND_LT 0x00000010 // LT checkbox
#define dTIME_COND_ENERGY 0x00000020 // energy checkbox
#define dTIME_COND_TEMP_BELOW 0x00000040 // time schedule is active only if temperature is below TempLimit (for dTIME_MODE_ENFORCE mode, Mx only)
#define dTIME_COND_TEMP_ABOVE 0x00000080 // time schedule is active only if temperature is above TempLimit (for dTIME_MODE_ENFORCE mode, Mx only)
#define dTIME_COND_TEMP (dTIME_COND_TEMP_BELOW | dTIME_COND_TEMP_ABOVE) // temperature checkbox (Mx only)

// Time schedule weekdays:
#define dTIME_WEEKDAY_MASK 0x0000FF00 // time schedule weekday mask
// Possible fields:
#define dTIME_WEEKDAY_ALL 0x0000FF00 // time schedule is active on all days
#define dTIME_WEEKDAY_MONDAY 0x00000100 // time schedule is active on Monday
#define dTIME_WEEKDAY_TUESDAY 0x00000200 // time schedule is active on Tuesday
#define dTIME_WEEKDAY_WEDNESDAY 0x00000400 // time schedule is active on Wednesday
#define dTIME_WEEKDAY_THURSDAY 0x00000800 // time schedule is active on Thursday
#define dTIME_WEEKDAY_FRIDAY 0x00001000 // time schedule is active on Friday
#define dTIME_WEEKDAY_SATURDAY 0x00002000 // time schedule is active on Saturday
#define dTIME_WEEKDAY_SUNDAY 0x00004000 // time schedule is active on Sunday

//New for Mx version 2.2, M version 4.1 and ECO version 3.1:

// Start time condition:
#define dTIME_EX_ON_MASK 0x00030000 // time schedule start time mask
// Possible values:
#define dTIME_EX_ON_TIME 0x00000000 // time schedule starts at given time
#define dTIME_EX_ON_SUNRISE 0x00010000 // time schedule starts at sunrise
#define dTIME_EX_ON_SUNSET 0x00020000 // time schedule starts at sunset

// Stop time condition:
#define dTIME_EX_OFF_MASK 0x000C0000 // time schedule stop time mask
// Possible values:
#define dTIME_EX_OFF_TIME 0x00000000 // time schedule stops at given time
#define dTIME_EX_OFF_SUNRISE 0x00040000 // time schedule stops at sunrise
#define dTIME_EX_OFF_SUNSET 0x00080000 // time schedule stops at sunset

// Binary input condition:
#define dTIME_EX_BIN_MASK 0x00700000 // time schedule binary input mask
// Possible fields:
#define dTIME_EX_BIN_INPUT 0x00100000 // binary input checkbox
#define dTIME_EX_BIN_INPUT_COND 0x00200000 // binary input condition (0..on, 1..off)
#define dTIME_EX_BIN_INPUT_RESERVED 0x00400000 // reserved field
