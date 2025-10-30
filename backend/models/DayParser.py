"""
Utility class to parse and compare days of operation
Handles two formats:
1. Comma-separated: "Mon,Wed,Fri" 
2. Dash/Range: "Fri-Sun" (means Friday, Saturday, Sunday)
3. Daily: "Daily" (means all days)
"""

class DayParser:
    # Day name mappings
    DAY_NAMES = {
        'monday': 'Mon',
        'tuesday': 'Tue', 
        'wednesday': 'Wed',
        'thursday': 'Thu',
        'friday': 'Fri',
        'saturday': 'Sat',
        'sunday': 'Sun',
        'mon': 'Mon',
        'tue': 'Tue',
        'wed': 'Wed',
        'thu': 'Thu',
        'fri': 'Fri',
        'sat': 'Sat',
        'sun': 'Sun'
    }
    
    # Day order for range expansion
    DAY_ORDER = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    @staticmethod
    def normalize_day(day):
        """Normalize day name to short format (Mon, Tue, etc.)"""
        day_clean = day.strip().lower()
        return DayParser.DAY_NAMES.get(day_clean, day.strip())
    
    @staticmethod
    def expand_range(start_day, end_day):
        """
        Expand a day range like 'Fri-Sun' to ['Fri', 'Sat', 'Sun']
        """
        start_day = DayParser.normalize_day(start_day)
        end_day = DayParser.normalize_day(end_day)
        
        try:
            start_idx = DayParser.DAY_ORDER.index(start_day)
            end_idx = DayParser.DAY_ORDER.index(end_day)
            
            # Handle wrap-around (e.g., Sat-Mon means Sat, Sun, Mon)
            if start_idx <= end_idx:
                return DayParser.DAY_ORDER[start_idx:end_idx + 1]
            else:
                return DayParser.DAY_ORDER[start_idx:] + DayParser.DAY_ORDER[:end_idx + 1]
        except ValueError:
            return []
    
    @staticmethod
    def parse_days(days_string):
      
        if not days_string or not isinstance(days_string, str):
            return []
        
        days_string = days_string.strip()
        
        # Handle "Daily"
        if days_string.lower() == 'daily':
            return DayParser.DAY_ORDER.copy()
        
        # Check for range format (contains dash)
        if '-' in days_string:
            parts = days_string.split('-')
            if len(parts) == 2:
                return DayParser.expand_range(parts[0], parts[1])
        
        # Handle comma-separated format
        if ',' in days_string:
            days = [DayParser.normalize_day(d) for d in days_string.split(',')]
            return [d for d in days if d in DayParser.DAY_ORDER]
        
        # Single day
        normalized = DayParser.normalize_day(days_string)
        if normalized in DayParser.DAY_ORDER:
            return [normalized]
        
        return []
    
    @staticmethod
    def days_match(user_selected_days, connection_days_string):
      
        if not user_selected_days or not connection_days_string:
            return False
        
        # Normalize user's selected days
        normalized_user_days = set([DayParser.normalize_day(d) for d in user_selected_days])
        
        # Parse connection's operating days
        connection_days = set(DayParser.parse_days(connection_days_string))
        
        # Exact match: connection must operate ONLY on selected days (no more, no less)
        return normalized_user_days == connection_days
