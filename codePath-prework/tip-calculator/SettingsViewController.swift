//
//  SettingsViewController.swift
//  tip-calculator
//
//  Created by Alex Kim on 12/25/21.
//

import UIKit

class SettingsViewController: UIViewController {

    //first tip text value
    @IBOutlet weak var firstDefTip: UITextField!
    
    //second tip text value
    @IBOutlet weak var secondDefTip: UITextField!
    
    //third tip text value
    @IBOutlet weak var thirdDefTip: UITextField!
    
    //Toggle for dark mode
    @IBOutlet weak var darkMode: UISwitch!
    
    //using the user default feature

    let def = UserDefaults.standard
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        darkMode.isOn = def.bool(forKey: "darkModeOn")
    }
    
    //set the previous default tip values when the screen appears
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        if def.bool(forKey: "darkModeOn") {
            overrideUserInterfaceStyle = .dark
        } else {
            overrideUserInterfaceStyle = .light
        }
        firstDefTip.text = String(Int(def.double(forKey: "defTip1") * 100))
        secondDefTip.text = String(Int(def.double(forKey: "defTip2") * 100))
        thirdDefTip.text = String(Int(def.double(forKey: "defTip3") * 100))
    }
    
    //set the new default value for tip slot 1
    @IBAction func newFirstTip(_ sender: Any) {
        let newTip = Double(firstDefTip.text!) ?? 15
        def.set(newTip/100, forKey: "defTip1")
        print(newTip)
        def.set(String(Int(newTip)) + "%", forKey: "def1Title")
    }
    
    //set the new default value for tip slot 2
    
    @IBAction func newSecondTip(_ sender: Any) {
        let newTip = Double(secondDefTip.text!) ?? 18
        def.set(newTip/100, forKey: "defTip2")
        print(newTip)
        def.set(String(Int(newTip)) + "%", forKey: "def2Title")
    }
    
    //set the new default value for tip slot 3
        
    @IBAction func newThirdTip(_ sender: Any) {
        let newTip = Double(thirdDefTip.text!) ?? 20
        def.set(newTip/100, forKey: "defTip3")
        def.set(String(Int(newTip)) + "%", forKey: "def3Title")
    }
    
    //switch toggle
    
    @IBAction func switchToggle(_ sender: UISwitch) {
        if sender.isOn {
            overrideUserInterfaceStyle = .dark
            def.set(true, forKey: "darkModeOn")
        } else {
            overrideUserInterfaceStyle = .light
            def.set(false, forKey: "darkModeOn")
        }
    }
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
