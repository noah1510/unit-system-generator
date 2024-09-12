#[cfg(test)]
mod tests {
    #[test]
    fn test_compilation() {
        let t1 = unit_system::Time::second(1.0);
        let t2 = unit_system::Time::second(2.0);
        
        println!("t1({}) + t2({}) = {}", t1, t2, t1 + t2);
        println!("t1({}) - t2({}) = {}", t1, t2, t1 - t2);
        println!("t1({}) / t2({}) = {}", t1, t2, t1 / t2);

        println!("t1({}) > t2({}) = {}", t1, t2, t1 > t2);
        println!("t1({}) < t2({}) = {}", t1, t2, t1 < t2);
        println!("t1({}) == t2({}) = {}", t1, t2, t1 == t2);
        println!("t1({}) * 2.0 == t2({}) = {}", t1, t2, (t1 * 2.0) == t2);

        println!("t1({}) * 2.0 = {}", t1, t1 * 2.0);
        println!("2.0 * t1({}) = {}", t1, 2.0 * t1);
        println!("t1({}) / 2.0 = {}", t1, t1 / 2.0);

        println!("-t1({}) = {}", t1, -t1);

        println!("min(t1, t2) = {}", std::cmp::min(t1, t2));
        println!("max(t1, t2) = {}", std::cmp::max(t1, t2));
    }
}
