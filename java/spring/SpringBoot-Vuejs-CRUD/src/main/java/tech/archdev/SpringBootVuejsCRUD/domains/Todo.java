package tech.archdev.SpringBootVuejsCRUD.domains;


import lombok.*;

import javax.persistence.*;

@Entity
@Data
@NoArgsConstructor
public class Todo {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NonNull
    @Column(name = "title")
    private String title;

    @Column(name = "completed")
    private Boolean completed=false;
}
