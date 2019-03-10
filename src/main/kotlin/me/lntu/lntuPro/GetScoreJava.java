package me.lntu.lntuPro;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class GetScoreJava {
    public List<String> scores = new ArrayList<>();
    private Document html;

    public GetScoreJava(String cookie) throws IOException {
        this.getHtml(cookie);
        this.parseHtml();
    }

    private void getHtml(String cookie) throws IOException {
        String scoreUrl = "http://10.21.24.120:11182/newacademic/student/queryscore/queryscore.jsdo?groupId=&moduleId=2020";
        html = Jsoup.connect(scoreUrl).cookie("JSESSIONID", cookie.substring(11)).get();
    }

    private void parseHtml() {
        Elements elements = html.getElementsByClass("infolist_common");

        for (Element each : elements) {
            String info = each.children().get(1).text() + each.children().get(3).text();
            scores.add(info);
        }
    }

}
