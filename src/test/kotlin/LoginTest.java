import me.lntu.lntuPro.GetScoreJava;
import me.lntu.lntuPro.Getscore;
import me.lntu.lntuPro.Login;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class LoginTest {
    public static void main(String[] args) throws IOException {
        String scoreUrl = "http://10.21.24.120:11182/newacademic/student/queryscore/queryscore.jsdo?groupId=&moduleId=2020";
        // Login login = new Login("1710030215", "");
        // String cookie = login.getCookie();

        String cookie = "JSESSIONID=A53AE1C12E83D8009D7C4862AEA31FD6.T55";
        GetScoreJava getScoreJava = new GetScoreJava(cookie);
        System.out.println("所有成绩: " + getScoreJava.scores);

    }
}
