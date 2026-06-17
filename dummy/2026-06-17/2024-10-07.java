import UIKit

class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        print("Xin chào iOS (và bug)")
    }
}

class Bug {
    private String description;
    private Severity severity;
    private Developer assignee;
}

