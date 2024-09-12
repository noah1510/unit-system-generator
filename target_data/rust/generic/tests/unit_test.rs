#[macro_use]
extern crate approx;

#[cfg(test)]
mod tests {
    #[test]
    fn test_literals() {
        let t1 = unit_system::Time::second(1.0);
        let t2 = unit_system::Time::millisecond(1000.0);
        let t3 = unit_system::Time::millisecond(1.0);

        assert_relative_eq!(t1, t2);
        assert_relative_eq!(t2, t1);

        assert_relative_eq!(t1, t3 * 1000.0);
        assert_relative_eq!(t3 * 1000.0, t1);
        assert_relative_eq!(t1, 1000.0 * t3);
        assert_relative_eq!(1000.0 * t3, t1);

        assert_relative_eq!(t3, t1 / 1000.0);
        assert_relative_eq!(t1 / 1000.0, t3);
        assert_relative_eq!(t3, t2 / 1000.0);
        assert_relative_eq!(t2 / 1000.0, t3);

        assert_relative_eq!(t1 / t2, 1.0);
        assert_relative_eq!(t2 / t1, 1.0);
        assert_relative_eq!(t1 / t3, 1000.0);
        assert_relative_eq!(t2 / t3, 1000.0);
        assert_relative_eq!(t3 / t1, 0.001);
        assert_relative_eq!(t3 / t2, 0.001);

        assert_relative_eq!(-t1 / t2, -1.0);
        assert_relative_eq!(-t2 / t1, -1.0);
        assert_relative_eq!(t1 / -t2, -1.0);
        assert_relative_eq!(t2 / -t1, -1.0);

        assert_relative_ne!(t1, unit_system::Time::millisecond(999.0));
        assert_relative_ne!(unit_system::Time::millisecond(999.0), t1);

        assert_relative_ne!(t1, unit_system::Time::millisecond(1.0) * 999.0);
        assert_relative_ne!(unit_system::Time::millisecond(1.0) * 999.0, t1);

        assert_relative_ne!(-t1, t2);
        assert_relative_ne!(-t2, t1);
        assert_relative_ne!(-t1, t1);
        assert_relative_ne!(-t2, t2);
    }

    #[test]
    fn test_combinations() {
        let t1 = unit_system::Time::second(1.0);
        let s1 = unit_system::Length::metre(10.0);
    
        let v1 = s1 / t1;
        assert_relative_eq!(v1, unit_system::Speed::mps(10.0));
        assert_relative_eq!(unit_system::Speed::mps(10.0), v1);


        let t2 = unit_system::Time::hour(10.0);
        let s2 = unit_system::Length::km(250.0);
    
        let v2 = s2 / t2;
        assert_relative_eq!(v2, unit_system::Speed::kmph(25.0));
        assert_relative_eq!(unit_system::Speed::kmph(25.0), v2);
    

        let v3 = unit_system::Speed::kmph(3.6).convert_multiplier(1.0);
        assert_relative_eq!(v3, unit_system::Speed::mps(1.0));
        assert_relative_eq!(unit_system::Speed::mps(1.0), v3);
    
        assert_relative_eq!(v3 * t1, t1 * v3);
        assert_relative_eq!(v3 * t2, t2 * v3);

        
        let a1 = s1 * s2;
        assert_relative_eq!(a1, unit_system::Area::m2(2500000.0));
        assert_relative_eq!(unit_system::Area::m2(2500000.0), a1);

        let a2 = unit_system::Area::m2(100.0);
        assert_relative_eq!(a2, unit_system::square(s1));
        assert_relative_eq!(unit_system::square(s1), a2);
        assert_relative_eq!(a2, s1 * s1);
        assert_relative_eq!(s1 * s1, a2);

        assert_relative_eq!(s1, unit_system::sqrt(a2));
        assert_relative_eq!(unit_system::sqrt(a2), s1);
        assert_relative_eq!(s1, a2 / s1);
    }

    # [test]
    fn test_comparisons(){
        let s1 = unit_system::Length::metre(1.0);
        let s2 = unit_system::Length::centimetre(1.0);
        let s3 = unit_system::Length::centimetre(2.0);

        assert!(s1 > s2);
        assert!(s2 < s1);
        assert!(s1 > s3);
        assert!(s3 < s1);
        assert!(s3 > s2);
        assert!(s2 < s3);
    }
}
