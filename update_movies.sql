-- Commandes SQL pour mettre à jour les informations des films
-- Base de données: Cinemacousas

-- 1. The Creator (ID: 6)
UPDATE movie 
SET 
    name = 'The Creator',
    duration = 133,
    director = 'Gareth Edwards',
    cast = 'John David Washington, Madeleine Yuna Voyles, Gemma Chan, Allison Janney, Ken Watanabe, Sturgill Simpson',
    synopsis = 'Dans un futur proche, au milieu d''une guerre entre les humains et les forces de l''intelligence artificielle, Joshua, un ancien agent des forces spéciales en deuil de sa femme disparue, est recruté pour traquer et tuer le Créateur, l''architecte insaisissable de l''IA avancée qui a développé une arme mystérieuse capable de mettre fin à la guerre... et à l''humanité elle-même.'
WHERE id = 6;

-- 2. Interstellar (ID: 5)
UPDATE movie 
SET 
    name = 'Interstellar',
    duration = 169,
    director = 'Christopher Nolan',
    cast = 'Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine, Casey Affleck, Wes Bentley, Topher Grace',
    synopsis = 'Dans un futur proche, la Terre se meurt et l''humanité fait face à l''extinction. Un groupe d''explorateurs franchit un trou de ver près de Saturne pour explorer des mondes lointains dans l''espoir de sauver l''espèce humaine. Cooper, un ancien pilote de la NASA devenu fermier, accepte de mener cette mission spatiale périlleuse, laissant derrière lui sa fille Murph.'
WHERE id = 5;

-- 3. Saw (ID: 7)
UPDATE movie 
SET 
    name = 'Saw',
    duration = 103,
    director = 'James Wan',
    cast = 'Cary Elwes, Danny Glover, Monica Potter, Michael Emerson, Ken Leung, Tobin Bell, Leigh Whannell',
    synopsis = 'Deux hommes se réveillent enchaînés dans une salle de bain délabrée. Entre eux gît un cadavre tenant un revolver et un magnétophone. Ils découvrent qu''ils sont les victimes du tueur en série Jigsaw, qui place ses victimes dans des situations où elles doivent choisir entre s''infliger de terribles mutilations ou mourir. Pour survivre, l''un d''eux devra tuer l''autre avant 18h00.'
WHERE id = 7;

-- 4. Avatar (ID: 8)
UPDATE movie 
SET 
    name = 'Avatar',
    duration = 162,
    director = 'James Cameron',
    cast = 'Sam Worthington, Zoe Saldana, Sigourney Weaver, Stephen Lang, Michelle Rodriguez, Giovanni Ribisi, Joel David Moore',
    synopsis = 'En 2154, Jake Sully, un ancien marine paraplégique, est envoyé sur Pandora, une lune luxuriante d''une planète lointaine, pour participer au programme Avatar. En contrôlant un corps hybride Na''vi-humain, il peut respirer l''air toxique de Pandora. Tiraillé entre suivre les ordres et protéger le monde qu''il considère comme son foyer, Jake doit choisir son camp lors d''un conflit épique qui décidera du sort de toute la planète.'
WHERE id = 8;

-- Vérification des mises à jour
SELECT id, name, duration, director, LEFT(synopsis, 100) as synopsis_preview
FROM movie 
WHERE id IN (5, 6, 7, 8)
ORDER BY name;
