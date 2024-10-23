use std::io;

// Utility function
fn remove_whitespace(s: String) -> String {
    s.split_whitespace().collect()
}

// Read user input
fn main() {
    let mut input = String::new();
    println!("Ready for user input.");
    match io::stdin().read_line(&mut input) {
        Ok(_) => {
            weird_algorithm(remove_whitespace(input).parse().unwrap());
        }
        Err(error) => println!("error: {error}"),
    }
}

fn weird_algorithm(num: i32) {
    if num == 1 {
        print!("{:?}", num);
        return;
    } else {
        print!("{:?} -> ", num);
        let new_num = if num % 2 == 0 { num / 2 } else { num * 3 + 1 };
        weird_algorithm(new_num);
    }
}
