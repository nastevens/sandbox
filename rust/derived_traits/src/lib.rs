use tower_service::Service;

pub trait Test<Request>: Service<Request> {
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
