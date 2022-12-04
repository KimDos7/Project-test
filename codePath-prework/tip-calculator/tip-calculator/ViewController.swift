//
//  ViewController.swift
//  tip-calculator
//
//  Created by Alex Kim on 12/25/21.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var billAmountTextField: UITextField!
    @IBOutlet weak var tipAmountLabel: UILabel!
    @IBOutlet weak var tipControl: UISegmentedControl!
    @IBOutlet weak var totalLabel: UILabel!
    
    let defaults = UserDefaults.standard
    
    //sets default tip values and the segment titles
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        self.title = "Tip Calculator"
//        defaults.set(0.15, forKey: "defTip1")
//        defaults.set(0.18, forKey: "defTip2")
//        defaults.set(0.2, forKey: "defTip3")
//        defaults.set("15%", forKey: "def1Title")
//        defaults.set("18%", forKey: "def2Title")
//        defaults.set("20%", forKey: "def3Title")
    }
    
    //on apperance from other pages, it updates the values for segment titles
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        if defaults.bool(forKey: "darkModeOn") {
            overrideUserInterfaceStyle = .dark
        } else {
            overrideUserInterfaceStyle = .light
        }
        let title1 = defaults.string(forKey: "def1Title") ?? "15"
        tipControl.setTitle(title1, forSegmentAt: 0)
        let title2 = defaults.string(forKey: "def2Title") ?? "18"
        tipControl.setTitle(title2, forSegmentAt: 1)
        let title3 = defaults.string(forKey: "def3Title") ?? "20"
        tipControl.setTitle(title3, forSegmentAt: 2)
        calculate()
    }
    
    //calcualte function that can be used for other funtions
    func calculate() {
        let bill = Double(billAmountTextField.text!) ?? 0

        let tipPercentages = [defaults.double(forKey: "defTip1") , defaults.double(forKey: "defTip2") , defaults.double(forKey: "defTip3")]
        let tip = bill * tipPercentages[tipControl.selectedSegmentIndex]
        let total = bill + tip

        tipAmountLabel.text = String(format: "$%.2f", tip)
        totalLabel.text = String(format: "$%.2f", total)
    }
    
    //method on how to calculate tip
    @IBAction func calculateTip(_ sender: Any) {
        calculate()
    }

    //calculates tip on the event that the bill amount field changes
    @IBAction func automaticTotalUpdate(_ sender: Any) {
        calculate()
    }
    
}

