import { Component, useState, xml, markup } from "@odoo/owl";
import { Counter } from "./components/Counter/Counter";
import { Card } from "./components/Card/Card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.text1 = "This is the content for card 1.";
        this.text2 = markup("<div class='text-success'>This is the content for card 2.</div>");
        this.sum = useState({ value: 0 });
    }

    incrementSum = () => {
        this.sum.value++;
    }
}
