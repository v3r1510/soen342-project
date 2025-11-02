class DayParser:

    
    # Mapping of day names to abbreviations
    DAY_NAMES = {
        'monday': 'Mon', 'mon': 'Mon',
        'tuesday': 'Tue', 'tue': 'Tue',
        'wednesday': 'Wed', 'wed': 'Wed',
        'thursday': 'Thu', 'thu': 'Thu',
        'friday': 'Fri', 'fri': 'Fri',
        'saturday': 'Sat', 'sat': 'Sat',
        'sunday': 'Sun', 'sun': 'Sun'
    }
    
    # Order of days for range expansion
    DAY_ORDER = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    @staticmethod
    def normalize_day(day_str):
     
        day_lower = day_str.strip().lower()
        return DayParser.DAY_NAMES.get(day_lower, day_str.strip())
    
    @staticmethod
    def expand_range(start_day, end_day):
  
        start_day = DayParser.normalize_day(start_day)
        end_day = DayParser.normalize_day(end_day)
        
        try:
            start_idx = DayParser.DAY_ORDER.index(start_day)
            end_idx = DayParser.DAY_ORDER.index(end_day)
            
            if start_idx <= end_idx:
                return DayParser.DAY_ORDER[start_idx:end_idx + 1]
            else:
                # Wrap around (e.g., Sat-Mon)
                return DayParser.DAY_ORDER[start_idx:] + DayParser.DAY_ORDER[:end_idx + 1]
        except ValueError:
            return [start_day, end_day]
    
    @staticmethod
    def parse_days(days_str):
   
        if not days_str or not isinstance(days_str, str):
            return []
        
        days_str = days_str.strip()
        
        # Handle "Daily" case
        if days_str.lower() == 'daily':
            return DayParser.DAY_ORDER.copy()
        
        # Check if it's a range (contains dash but not comma)
        if '-' in days_str and ',' not in days_str:
            parts = days_str.split('-')
            if len(parts) == 2:
                return DayParser.expand_range(parts[0], parts[1])
        
        # Handle comma-separated list
        if ',' in days_str:
            days = [DayParser.normalize_day(d) for d in days_str.split(',')]
            return days
        
        # Single day
        return [DayParser.normalize_day(days_str)]
    
    @staticmethod
    def days_match(user_days, connection_days_str):
     
        if not user_days or not connection_days_str:
            return True  # No filter applied
        
        # Parse connection days
        connection_days = DayParser.parse_days(connection_days_str)
        
        # Normalize user days
        normalized_user_days = [DayParser.normalize_day(d) for d in user_days]
        
        # EXACT matching: sets must be equal
        return set(normalized_user_days) == set(connection_days)
