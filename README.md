# **Giới thiệu bài Project cuối kỳ môn trí tuệ nhân tạo nhóm 9**

## Thành viên nhóm 9:
Lưu Quang Tiến - 23110157\
Trần Cẩm Long - 23110122

## **Mục tiêu của Project**
Bài Project cuối kỳ thực hiện xây dựng game Snakes! bằng ngôn ngữ Python nhằm mục đích biểu diễn cách ứng dụng các thuật toán đã được học trong việc tìm kiếm đường đi ngắn nhất để tìm mục tiêu. Từ đó tìm ra thuật toán nào phù hợp, tối ưu nhất trong việc tìm kiếm đường đi ngắn nhất đến mục tiêu trong trò chơi.

## **Mục lục**
Trong phần giới thiệu của Project, chúng em sẽ nói qua về những chủ đề sau:
- [Thư viện](#thư-viện)
- [Giới thiệu game Snakes!](#giới-thiệu-game-Snakes)
- [Lý thuyết, nguyên lý cơ bản của thuật toán](#lý-thuyết-nguyên-lý-cơ-bản-của-thuật-toán)
- [Demo các thuật toán](#demo-các-thuật-toán)
- [Ưu điểm, nhược điểm](#ưu-điểm-nhược-điểm)
- [Thuật toán tối ưu nhất](#thuật-toán-tối-ưu-nhất)
- [Kết luận](#kết-luận)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## *Thư viện*
Trong quá trình xậy dựng game, nhóm có sử dụng những thư viện không có sẵn trong python:
- pygame: thư viện cốt lõi trong quá trình thực hiện Project, cung cấp những công cụ để tạo GUI và thực hiện vòng lặp để game hoạt động.
- openpyxl: thư viện cung cấp công cụ giúp xuất dữ liệu trong quá trình sử dụng thuật toán để chạy game tự động.

## *Giới thiệu game Snakes!*
Lý do nhóm 9 lựa chọn game Snakes! hay thường biết đến là "Rắn săn mồi" là vì đây là một trò chơi phổ biến và khá quen thuộc đối với nhiều người, đồng thời cũng rất dễ để hiểu được quy trình tìm đường đi của con rắn đến thức ăn.

Luật chơi của Snakes! rất đơn giản. Người chơi điều khiển con rắn di chuyển theo 4 chiều, tương ứng với 4 nút chỉ hướng trên bàn phím, giúp con rắn ăn được quả táo để nó dài ra và giúp con rắn tránh va chạm vào các chướng ngại vật (tường, lề màn hình, và quan trọng nhất là cơ thể con rắn).

## *Lý thuyết, nguyên lý cơ bản của thuật toán*

### BFS
Thuật toán quét cạn bắt đầu từ đầu con rắn đến quả táo. Con rắn sẽ quét cạn bắt đầu từng lớp, kiểm tra đã đến đích chưa, sau đó sinh ra các trạng thái (ô) con an toàn với hàm snake.Is_safe() rồi đưa vào hàng đợi nếu chưa được duyệt qua. Sau khi tìm kiếm được mục tiêu, thuật toán sẽ xây dựng lại đường đi từ quả táo đến đầu con rắn để dẫn đường cho nó di chuyển.
Độ phức tạp trường hợp xấu nhất:
- Không gian: 24 x 15 = 360
- Thời gian: 24 x 15 = 360

![BFS_pathfinding](asset/BFS.png)

### DFS
Thuật toán tìm kiếm theo chiều sâu bắt đầu từ đầu con rắn đến quả táo. Con rắn sẽ kiểm tra đã đến đích chưa, sau đó sinh ra các trạng thái (ô) con an toàn với hàm snake.Is_safe() rồi đưa vào hàng đợi nếu chưa được duyệt qua. Các ô con được duyệt qua theo FIFO (First in first out), khác với BFS quét cạn, DFS tìm kiếm theo nhánh sâu. Sau khi tìm kiếm được mục tiêu, thuật toán sẽ xây dựng lại đường đi từ quả táo đến đầu con rắn để dẫn đường cho nó di chuyển.
Độ phức tạp trường hợp xấu nhất:
- Không gian: 360
- Thời gian: 360

![DFS_pathfinding](asset/DFS.png)

### UCS
Thuật toán UCS khác biệt với những thuật toán trước ở việc kèm theo chi phí g(n) cho các trạng thái và từ đó tìm đường đi với chi phí ít nhất. Môi trường game được đặt những khu vực với các mức độ "nguy hiểm" (+0, +1, +2, +3) và từ đó quyết định được đường đi cuối dùng ngắn và an toàn nhất cho con rắn.
Độ phức tạp trường hợp xấu nhất:
- Không gian: 360
- Thời gian: 360log(360)

![UCS_pathfinding](asset/UCS.png)

## Greedy
Khác với những thuật toán trước, Greedy sử dụng heuristic h(n) để tìm đường đi tốt nhất tại thời điểm đó và đi đến quả táo. Trong Project, heuristic được kết hợp giữa 3 hàm tính toán. Flood fill từ quả táo đến đầu con rắn, Flood fill từ đuôi con rắn đến đầu con rắn giúp rắn tránh việc tự kẹt mình (bằng cách đuổi theo đuôi) và Flood fill để phạt con rắn khi nó đi vào những vị trí hẹp có thể làm nó bị kẹt.
Độ phức tạp trường hợp xấu nhất:
- Không gian: 360
- Thời gian: 360log(360)


### Beam search
Beam search cốt lõi cũng hoạt động tương tự như thuật toán Greedy, nhưng khác với Greedy chỉ lấy 1 lựa chọn tốt nhất, Beam search sẽ lấy số bước đi tốt nhất tại thời điểm đó tương ứng với độ rộng của beam đã được khai báo trước.
Độ phức tạp trường hợp xấu nhất, với độ rộng của beam = 3:
- Không gian: 360 + 3 = 363
- Thời gian: 360 x 3 = 1080


### Simulated annealing
Thuật toán Simulated anneling tìm kiếm quả táo bằng cách tìm kiếm đường đi cho đến khi con rắn tìm thấy được mục tiêu hoặc nhiệt độ T bị nguội đến mức đã khai báo trước, khi đó con rắn sẽ di chuyển tới vị trí tốt nhất đã tìm được trong vòng lặp và sẽ tiếp tục tìm kiếm quả táo tại vị trí đó. Điều này lặp lại cho đến khi con rắn tìm thấy quả táo hoặc không thể tìm kiếm nữa. Trong quá trình tìm kiếm, nếu như không tìm thấy đường đi tốt hơn, son rắn sẽ dựa vào nhiệt độ T và độ nguội alpha để lựa chọn ngẫu nhiên bước đi tiếp theo.
Độ phức tạp trường hợp xấu nhất:
- Không gian: 1
- Thời gian: 360


### Không gian không nhìn thấy
Thuật toán không gian không nhìn thấy theo nhóm em đánh giá là một thuật toán không phù hợp cho quá trình mô phỏng/ tìm kiếm đường đi cho con rắn đến quả táo. Với 1 môi trường lớn (24x15), con rắn không biết được trạng thái bản thân hiện tại và vị trí của mục tiêu, đồng thời với sự biến đổi môi trường (thân con rắn di chuyển), những điều này làm cho việc tìm kiếm đường đi con rắn cực kỳ tốn kém cả về tài nguyên và thời gian.
Độ phức tạp trường hợp xấu nhất, độ dài rắn L:
- Không gian: 360*L*L!
- Thời gian: 360*L*L!


### Không gian nhìn thấy một phần
Đối với tìm kiếm đường đi bằng không gian chỉ nhìn thấy một phần, con rắn không nhìn thấy được mọi thứ nhưng khác với khi không nhìn thấy gì hết, nó có thể dựa vào môi trường nó có thể nhìn thấy để rút ngắn số lượng trạng thái, bước đi mà con rắn cần phải duyệt qua. Nhưng mặc dù cũng đã giảm đi số lượng đường đi, nó vẫn gặp lại vấn đề giống tìm kiếm đường đi trong không gian không nhìn thấy gì, việc con rắn liên tục di chuyển làm số lượng trạng thái niềm tin cho con rắn bùng nổ lên, nên việc tìm kiếm trong môi trường nhìn thấy một phần bằng trạng thái niềm tin là không khả thi. Nhưng nhóm 9 đã sử dụng heuristic để dẫn đường cho con rắn, tìm đường dựa vào vùng nhìn thấy của con rắn. Nếu con rắn nhìn thấy táo, nó sẽ đặt heuristic bằng flood fill để tìm kiếm đường đi ngắn nhất, nếu không nhìn thấy, ta tăng heuristic cho quả táo một giá trị lớn. Nếu những ô càng gần táo và liền kề ít với những ô không nằm trong vùng nhìn thấy thì heuristic càng nhỏ. Từ đó có thể sử dụng Greedy để tìm kiếm quả táo, điều này có thế rút gọn số lượng lớn trạng thái, đường đi mà con rắn cần phải duyệt qua.
Độ phức tạp trường hợp xấu nhất, độ rộng tầm nhìn: 5:
- Không gian: 360
- Thời gian: 360 x 5x5 = 9000


### Backtracking
Thuật toán Backtracking là một thuật toán đơn giản, sử dụng đề quy để duyệt qua các trạng thái, đường đi. Trong thuật toán Backtracking của nhóm 9, trước khi thực hiện bước đi, thì thuật toán có kiểm tra rằng buộc trước (tường, lề màn hình, thân con rắn), làm giảm số lượng bước đi con rắn phải duyệt qua. Tuy hơi tốn kém về thời gian và tài nguyên, Backtracking rất chính xác và dễ hiểu, có thể áp dụng một cách dễ dàng.
Độ phức tạp xấu nhất, với limmit = 10000:
- Không gian: 360
- Thời gian: 10000 do limmit


### AC3
Đối với game Snake!, thuật toán AC3 không phù hợp với việc tìm đường đi ngắn nhất đến quả táo. Với không gian trạng thái lớn (24x15), mỗi phần con rắn cần phải được duy trì domain, rằng buộc lên bản thân con rắn cực kỳ phức tạp và môi trường liên tục thay đổi bới sự di chuyển của con rắn. Những điều này làm cho việc tìm kiếm đường đi con rắn bằng thuật toán AC3 cực kỳ phức tạp, tốn kém và không khả thi.
Độ phức tạp trường hợp xấu nhất, độ dài rắn L:
- Không gian: không khả thi
- Thời gian: 360*L*L!

## *Demo các thuật toán*

### BFS
![BFS_demo](asset/BFS_demo.gif)

### DFS
![DFS_demo](asset/DFS_demo.gif)

### UCS
![UCS_demo](asset/UCS_demo.gif)

### Greedy
![Greedy_demo](asset/Greedy_demo.gif)

### Beam search
![Beam_demo](asset/Beam_demo.gif)

### Simulated annealing
![SimA_demo](asset/SimA_demo.gif)

### Không gian nhìn thấy một phần
![PO_demo](asset/PO_demo.gif)

### Backtracking
![Backtrack_demo](asset/Backtrack_demo.gif)

## *Ưu điểm, nhược điểm*

### BFS
* Ưu điểm:
  - Luôn cố tìm đường đi ngắn nhất đến quả táo.
  - Đơn giản, dễ áp dụng và sử dụng cùng các thuật toán khác.
* Nhược điểm:
  - Tiêu hao tài nguyên bộ nhớ.
  - Không tối ưu với những môi tường lớn và rắn dài.

### DFS
* Ưu điểm:
  - Không gian trạng thái nhỏ hơn BFS.
* Nhược điểm:
  - Không đảm bảo tìm được đường đi ngắn nhất đến quả táo.
  - Khi môi trường lớn, rắn dài thì độ phức tạp về thời gian cao.
  - Dễ lằm rắn bị mắc kẹt.

### UCS
* Ưu điểm:
  - Dựa vào những vùng an toàn, con rắn có thể tìm được đường đi an toàn nhất, tránh bị mắc kẹt hoặc hết đường đi.
* Nhược điểm:
  - Tiêu hao tài nguyên bộ nhớ.
  - Nếu chi phí các đường đi bằng nhau thì độ phức tạp về thời gian cao.

### Greedy
* Ưu điểm:
  - Tìm kiếm đường đi nhanh.
  - Lựa chọn được những bước đi tốt nhất ở thời điểm hiện tại.
  - Giảm thiểu không gian trạng thái cần phải duyệt, tiết kiệm thời gian.
* Nhược điểm:
  - Không đảm bảo tối ưu, rắn có thể bị mắc kẹt không tìm thấy đường đi tiếp theo.
  - Để thuật toán có thể hiệu quả, cần phải thiết kể heuristic một cách hợp lý.
  
### Beam search
* Ưu điểm:
  - Giống Greedy, sử dụng heuristic để tìm đường đi.
  - Tiết kiệm tài nguyên bộ nhớ hơn Greedy.
  - Giảm thiểu không gian trạng thái cần phải duyệt, tiết kiệm thời gian.
* Nhược điểm:
  - Không đảm bảo tối ưu, rắn có thể bị mắc kẹt không tìm thấy đường đi tiếp theo.
  - Để thuật toán có thể hiệu quả, cần phải thiết kể heuristic một cách hợp lý.
  - Nếu độ rộng của beam quá nhỏ thì có thể không tìm thấy đường đi.

### Simulated annealing
* Ưu điểm:
  - Tìm kiếm đường đi nhanh.
  - không gian trạng thái nhỏ.
  - Khắc phục được vấn đề mắc kẹt của local search bằng cách chấp nhận những bước đi không tối ưu.
* Nhược điểm:
  - Tùy thuộc vào nhiệt độ T và độ làm lạnh alpha mà hiệu suất tìm đường đi đến táo tăng hoặc giảm.
  - Đôi khi đường đi không khả thi với rắn dài.
  - Khi không tìm được đường đi đến táo, phải tìm lại đường đi bắt đầu từ vị trí tốt nhất vừa tìm được.

### Môi trường không nhìn thấy
* Ưu điểm:
  - Có thể tìm thấy đường đi đến quả táo ngay cả khi không nhìn thấy.
* Nhược điểm:
  - Không khả thi cho môi trường lớn, rắn dài.
  - Tiêu hao lớn về cả tài nguyên bộ nhớ, thời gian.
  - Phức tạp trong việc áp dụng.
  - Không phù hợp với game có môi trường động như Snake! \
=> Không nên sử dụng để tìm kiếm đường đi từ rắn đến táo.

### Môi trường nhìn thấy một phần
* Ưu điểm:
  - Khả thi đối với những môi trường lớn hơn.
  - Có sử dụng heuristic để khắc phục điểm yếu của tìm kiếm không nhìn thấy trong môi trường động.
* Nhược điểm:
  - Không đảm bảo tìm thấy đường đi ngắn nhất.
  - Để thuật toán có thể hiệu quả, cần phải thiết kể heuristic một cách hợp lý.

### Backtracking
* Ưu điểm:
  - Nếu không có giới hạn hoặc limmit được cho giá trị hợp lý, thuật toán sẽ luôn tìm thấy đường đi.
  - Có thể sử dụng heuristic để cải tiến thuật toán.
  - Đơn giản và dễ dàng áp dụng, kết hợp với thuật toán khác.
* Nhược điểm:
  - Độ phức tạp về thời gian trong trường hợp xấu nhất lớn.
  - Tiêu hao tài nguyên bộ nhớ.
  - Tùy vào giới hạn limmit, rắn có thể không tìm thấy đường đi đến quả táo.

### AC3
* Ưu điểm:
  - Loại bỏ được những không gian trạng thái không hợp lệ với rằng buộc.
  - Có thể kết hợp với những thuật toán khác, như Backtracking, ... để cải thiện hiệu quả quá trình tìm đường đi.
  - Cực kỳ tốt trong những môi trường có rằng buộc mạnh.
* Nhược điểm:
  - Cần phải thực hiện tính domain của rắn dài, phức tạp làm tốn kém tài nguyên thời gian, bộ nhớ.
  - Phức tạp trong việc áp dụng.
  - Không phù hợp với game có môi trường động như Snake! \
=> Không nên sử dụng để tìm kiếm đường đi từ rắn đến táo.

## *Thuật toán tối ưu nhất*

Sau khi thực hiện Demo tìm kiếm đường đi đến 10 quả táo, nhóm có dữ liệu số không gian trạng thái trung bình để tìm thấy đường đi đến mỗi quả táo cho mối thuật toán:
- BFS: 197.9 trạng thái
- DFS: 169.2 trạng thái
- UCS: 133 trạng thái
- Greedy: 16.4 trạng thái
- Beam search: 44.5 trạng thái
- Simulated annealing: 79.2 trạng thái
- Môi trường nhìn thấy một phần: 88.1 trạng thái
- Backtracking: 16.6 trạng thái \
=> Ta thấy rằng, khi xét số không gian trạng thái đã đi qua. Thuật toán Greedy là thuật toán tối ưu nhất trong các thuật toán đã đề cập để thực hiện game Snake!

## **Kết luận**
Qua Project này, những thành viên trong nhóm 9 đã hiểu biết thêm về những kiến thức về các thuật toán ứng dụng trong tìm kiếm đường đi. Đồng thời, cũng được bổ sung và bồi đắp thêm những kiến thức lập trình ngôn ngữ Python cùng với những thư viện và công cụ ngôn ngữ cung cấp. Tuy Project có thể chưa được tối ưu, thẩm mỉ nhưng những kinh nghiệm chúng em đạt được từ quá trính thực hiện sẽ đi theo suốt quá trình học tập và tìm kiếm, thực hiện việc làm trong tương lai chúng em.

Phương hướng cải thiện:
-	Bổ sung và cải thiện thuật toán: Cải tiến hàm heuristic để giúp rắn di chuyển mượt mà hơn
-	Nâng cấp giao diện và trải nghiệm người dùng
-	Tối ưu hiệu năng chương trình
-	Phát triển phiên bản mở rộng: tạo chế độ nhiều người chơi hoặc các AI đấu với nhau

## **Tài liệu tham khảo**
[1] *PyGame Beginner Tutorial in Python - Adding Buttons*, Coding With Russ, https://www.youtube.com/watch?v=G8MYGDf_9ho \
[2] *Snake Game in Python Tutorial with pygame(OOP)*, Programming With Nick, https://www.youtube.com/watch?v=1zVlRXd8f7g&t \
[3] Russell, S. (2016). *Artificial Intelligence: A Modern Approach, Third Edition*. Pearson Education
[4] Rembound. (2015, February 16). *Creating a snake game tutorial with HTML5*. Rembound. https://rembound.com/articles/creating-a-snake-game-tutorial-with-html5
